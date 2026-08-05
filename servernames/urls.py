from django.urls import include,path
from . import views

urlpatterns =[
path("", views.serverlist, name="serverlist"),
path("add/", views.serveradd, name="serveradd"),
path("<int:id>/edit/", views.serveredit, name="serveredit"),
path("<int:id>/delete/", views.serverdel, name="serverdel"),
path("active/", views.activeserver, name="activeserver"),
path("warning/", views.warningserver, name="warningserver"),
path("expired/", views.expiredserver, name="expiredserver"),]