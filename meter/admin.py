from django.contrib import admin
from .models import MeterReading

# Register your admins here.
admin.site.register(MeterReading)
list_display = ('client', 'meter', 'reading_date', 'reading_value')