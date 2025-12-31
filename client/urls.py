from django.urls import path
from .views import ClientListCreate, ClientRetrieveUpdateDelete

urlpatterns = [
    path('', ClientListCreate.as_view(), name='clients'),
    path('<int:id>/', ClientRetrieveUpdateDelete.as_view(), name='client-detail'),
]