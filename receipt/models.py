from django.db import models
from client.models import Client

# Create your models here.
class Receipt(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="receipts")
    date = models.DateTimeField(auto_now_add=True, null=True)
    meter_number = models.CharField(max_length=50, null=True)
    previous_reading = models.FloatField(null=True)
    current_reading = models.FloatField(null=True)
    units_consumed = models.FloatField(null=True)
    rate_per_unit = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    receipt_number = models.CharField(max_length=100, unique=True, null=True, blank=True)


    def __str__(self):
        return f"Receipt for {self.client.name}"