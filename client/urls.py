from django.urls import path
from .views import ClientListCreate, ClientRetrieveUpdateDelete

urlpattern = [
    path('client/', ClientListCreate.as_view(), name='clients'),
    path('client/<int:id>/', ClientRetrieveUpdateDelete.as_view(), name='client-detail'),
]