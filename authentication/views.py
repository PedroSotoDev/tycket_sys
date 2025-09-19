from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True 
    authentication_form = AuthenticationForm


def Pa(req):
    # return render(req, "login.html")
    return HttpResponse("hola")