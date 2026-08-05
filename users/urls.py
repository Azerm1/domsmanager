from django.urls import path
from . import views

urlpatterns = [
path("profil/", views.profil, name="profil"),
path("login/", views.user_login, name="login"),
path("logout/", views.user_logout, name="logout"),
path("edit/", views.usersedit, name="usersedit"),
]