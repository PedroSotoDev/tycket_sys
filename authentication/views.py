from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import RegisterForm
from django.shortcuts import render, redirect



class CustomLoginView(LoginView):
    template_name = "login/login.html"
    redirect_authenticated_user = True 
    authentication_form = AuthenticationForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("user_dashboard")
    else:
        form = RegisterForm()
    return render(request, "login/register.html", {"form": form})