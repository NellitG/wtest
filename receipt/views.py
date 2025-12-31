from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ReceiptSerializer
from .models import Receipt, Client, MeterReading
from rest_framework.views import APIView

# Create your views here.
# --- RECEIPTS ---
class ReceiptListCreate(generics.ListCreateAPIView):
    queryset = Receipt.objects.all().order_by("-date")
    serializer_class = ReceiptSerializer


class ReceiptsByClient(APIView):
    def get(self, request, client_id):
        receipts = Receipt.objects.filter(client_id=client_id).order_by("-date")
        serializer = ReceiptSerializer(receipts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReceiptRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Updating receipts is not allowed."},
            status=status.HTTP_400_BAD_REQUEST
        )


# --- NEW: Save receipt properly ---
class SaveReceiptForClient(APIView):
    """
    Creates a new receipt for a client based on current reading, previous reading, and rate.
    """

    def post(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({"detail": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get input
        current_reading = request.data.get("current_reading")
        rate_per_unit = request.data.get("rate_per_unit", 120)

        # Get previous reading
        last_reading = (
            MeterReading.objects.filter(client=client)
            .order_by("-date")
            .first()
        )
        previous_reading = float(last_reading.current_reading) if last_reading else 0

        # Validate
        try:
            current_reading = float(current_reading)
            rate_per_unit = float(rate_per_unit)
        except (TypeError, ValueError):
            return Response({"detail": "Invalid current reading or rate"}, status=status.HTTP_400_BAD_REQUEST)

        if current_reading < previous_reading:
            return Response({"detail": "Current reading cannot be less than previous reading"}, status=status.HTTP_400_BAD_REQUEST)

        units_consumed = current_reading - previous_reading
        amount = units_consumed * rate_per_unit

        receipt_data = {
            "client": client.id,
            "meter_number": last_reading.meter_number if last_reading else "",
            "previous_reading": previous_reading,
            "current_reading": current_reading,
            "units_consumed": units_consumed,
            "rate_per_unit": rate_per_unit,
            "amount": amount,
        }

        serializer = ReceiptSerializer(data=receipt_data)
        if serializer.is_valid():
            receipt = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    