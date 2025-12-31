from meter.views import DashboardStats, MeterReadingListCreate
from django.urls import path
from meter.views import MeterReadingRetrieveUpdateDelete
# from meter.views import LoginView

urlpatterns = [

    path("", MeterReadingListCreate.as_view(), name="meter_readings"),
    path("<int:id>/", MeterReadingRetrieveUpdateDelete.as_view(), name="reading_detail"),

    # path("dashboard-stats/", DashboardStats.as_view(), name="dashboard_stats"),
    # path("login/", LoginView.as_view(), name="login"),


]