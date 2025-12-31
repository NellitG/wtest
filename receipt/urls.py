from django.urls import path
from . import views

urlpatterns = [
   # Receipts
   path("receipts/", views.ReceiptListCreate.as_view(), name="receipts"),
   path("receipts/<int:id>/", views.ReceiptRetrieveUpdateDelete.as_view(), name="receipt_detail"),
   path("clients/<int:client_id>/receipts/save/", views.SaveReceiptForClient.as_view(), name="save_receipt"),
   path("clients/<int:client_id>/receipts/", views.ReceiptsByClient.as_view(), name="client_receipts"),


]