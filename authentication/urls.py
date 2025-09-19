from django.urls import path
from .views import Pa

urlpatterns = [
    path("/", Pa, name="login"),
]
