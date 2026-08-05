from django.urls import path
from . import views

urlpatterns =[
path("", views.domslist, name="domslist"),
path("add/", views.domsadd, name="domsadd"),
path("<int:id>/edit/", views.domsedit, name="domsedit"),
path("<int:id>/delete/", views.domsdel, name="domsdel"),
path("active/", views.activedoms, name="activedoms"),
path("warning/", views.warningdoms, name="warningdoms"),
path("expired/", views.expireddoms, name="expireddoms"),]