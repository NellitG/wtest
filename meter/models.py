from django.db import models
from client.models import Client

# Create your models here.
class MeterReading(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='readings')
    meter_number = models.CharField(max_length=100, blank=True, null=True)
    current_reading = models.DecimalField(max_digits=10, decimal_places=2)
    previous_reading = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    units_consumed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rate_per_unit = models.DecimalField(default=120.00, max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    RATE_PER_UNIT = 160  

    def save(self, *args, **kwargs):
        
        is_new = self.pk is None  

        # 🔹 Auto-fill previous reading
        if is_new:
            last_record = (
                MeterReading.objects.filter(client=self.client)
                .exclude(pk=self.pk)
                .order_by('-date')
                .first()
            )
            self.previous_reading = last_record.current_reading if last_record else 0

        # 🔹 Auto-fill meter number from client
        if self.client and hasattr(self.client, 'meter_number'):
            self.meter_number = self.client.meter_number

        # 🔹 Prevent invalid readings
        if self.current_reading < (self.previous_reading or 0):
            raise ValueError("Current reading cannot be less than previous reading.")

        # 🔹 Calculate values
        self.units_consumed = self.current_reading - (self.previous_reading or 0)
        self.amount = self.units_consumed * self.RATE_PER_UNIT

        # 🔹 Auto-generate receipt number if missing
        if not self.receipt_number:
            from datetime import datetime
            import uuid
            self.receipt_number = f"RCPT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:4].upper()}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.name} - {self.date}"