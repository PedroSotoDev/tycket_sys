from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('useradm/', views.useradm_dashboard, name='useradm_dashboard'),
    path('tickets/<int:ticket_id>', views.ticket_detalle, name='ticket_detalle'),
    
]