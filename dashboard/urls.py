from django.urls import path
from . import views
from django.urls import path
from .views import cron_check_expirations

urlpatterns =[
path("", views.dashboard, name="dashboard"),
path(
    "cron/check-expirations/",
    cron_check_expirations,
    name="cron_check_expirations",
),]