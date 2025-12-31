from meter.views import DashboardStats, MeterReadingListCreate
from django.urls import path
from meter.views import MeterReadingRetrieveUpdateDelete
from meter.views import LoginView

urlpatterns = [

    path("readings/", MeterReadingListCreate.as_view(), name="meter_readings"),
    path("readings/<int:id>/", MeterReadingRetrieveUpdateDelete.as_view(), name="reading_detail"),

    path("dashboard-stats/", DashboardStats.as_view(), name="dashboard_stats"),
    path("login/", LoginView.as_view(), name="login"),


]