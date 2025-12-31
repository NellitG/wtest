
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/meter/', include('meter.urls')),
    path('api/receipt/', include('receipt.urls')),
    path('api/client/', include('client.urls')),
]
