from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ReceiptSerializer
from .models import Receipt
from rest_framework.views import APIView

# Create your views here.
# --- RECEIPTS ---
class ReceiptListCreate(generics.ListCreateAPIView):
    queryset = Receipt.objects.all().order_by("-date")
    serializer_class = ReceiptSerializer

class ReceiptRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Updating receipts is not allowed."},
            status=status.HTTP_400_BAD_REQUEST
        )


