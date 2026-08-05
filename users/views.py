from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .userform import userform

def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def profil(request):
    return render(request, "profil.html", {
        "user": request.user
    })
    
@login_required
def usersedit(request):
    user = request.user
    if request.method == "POST":
        form = userform(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profil")
    else:
        form = userform(instance=user)
    return render(request, "usersedit.html", {
        "form": form
    })
def home(request):
    return redirect("login")