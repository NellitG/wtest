from django.urls import path
from . import views

urlpatterns = [
   # Receipts
   path("", views.ReceiptListCreate.as_view(), name="receipts"),
   path("<int:id>/", views.ReceiptRetrieveUpdateDelete.as_view(), name="receipt_detail"),


]