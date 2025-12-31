from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MeterReadingSerializer
from .models import MeterReading
from client.models import Client
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncMonth

# Create your views here.
class MeterReadingListCreate(generics.ListCreateAPIView):
    queryset = MeterReading.objects.all()
    serializer_class = MeterReadingSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MeterReadingRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeterReading.objects.all()
    serializer_class = MeterReadingSerializer
    lookup_field = "id"


# --- FETCH PREVIOUS READING ---
class ClientPreviousReading(APIView):
    def get(self, request, client_id):
        """Return the last reading value for the given client."""
        last_reading = (
            MeterReading.objects.filter(client_id=client_id)
            .order_by("-date")
            .first()
        )
        previous_value = float(last_reading.current_reading) if last_reading else 0
        return Response({"previous_reading": previous_value}, status=status.HTTP_200_OK)


# --- BILL CALCULATION ---
class CalculateBill(APIView):
    def post(self, request, client_id):
        """Calculate bill for a given client based on current reading."""
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        current_reading = request.data.get("current_reading")
        rate_per_unit = request.data.get("rate_per_unit", getattr(MeterReading, "RATE_PER_UNIT", 160))

        # Validate numeric inputs
        try:
            current_reading = float(current_reading)
            rate_per_unit = float(rate_per_unit)
        except (TypeError, ValueError):
            return Response({"error": "Invalid reading or rate"}, status=status.HTTP_400_BAD_REQUEST)

        last_reading = (
            MeterReading.objects.filter(client=client)
            .order_by("-date")
            .first()
        )
        previous_reading = float(last_reading.current_reading) if last_reading else 0

        if current_reading < previous_reading:
            return Response(
                {"error": "Current reading cannot be less than previous reading"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        units_consumed = current_reading - previous_reading
        total_amount = units_consumed * rate_per_unit

        return Response(
            {
                "client_id": client.id,
                "client": client.name,
                "previous_reading": previous_reading,
                "current_reading": current_reading,
                "units_consumed": units_consumed,
                "rate_per_unit": rate_per_unit,
                "amount": total_amount,
            },
            status=status.HTTP_200_OK,
        )


# --- DASHBOARD STATISTICS ---
class DashboardStats(APIView):
    """Aggregates system-wide dashboard analytics."""

    def get(self, request):
        total_clients = Client.objects.count()
        total_readings = MeterReading.objects.count()
        total_revenue = MeterReading.objects.aggregate(total=Sum("amount"))["total"] or 0

        now = timezone.now()
        current_month = now.month
        month_revenue = (
            MeterReading.objects.filter(date__month=current_month)
            .aggregate(total=Sum("amount"))
            .get("total")
            or 0
        )

        consumption_data = (
            MeterReading.objects.annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total_units=Sum("units_consumed"))
            .order_by("month")
        )
        consumption_months = [c["month"].strftime("%b %Y") for c in consumption_data]
        consumption_values = [float(c["total_units"] or 0) for c in consumption_data]

        revenue_data = (
            MeterReading.objects.annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total_amount=Sum("amount"))
            .order_by("month")
        )
        revenue_months = [r["month"].strftime("%b %Y") for r in revenue_data]
        revenue_values = [float(r["total_amount"] or 0) for r in revenue_data]

        data = {
            "total_clients": total_clients,
            "total_readings": total_readings,
            "total_revenue": total_revenue,
            "month_revenue": month_revenue,
            "monthly_consumption": {
                "months": consumption_months,
                "values": consumption_values,
            },
            "revenue_trend": {
                "months": revenue_months,
                "values": revenue_values,
            },
        }

        return Response(data)