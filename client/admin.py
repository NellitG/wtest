from django.contrib import admin
from .models import Client

# Register your models here.
admin.site.register(Client)
list_display = ('name', )