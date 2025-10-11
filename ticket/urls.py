from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('useradm/', views.useradm_dashboard, name='useradm_dashboard'),
    path('tickets/<int:ticket_id>', views.ticket_detalle, name='ticket_detalle'),
    path('tickets/eliminar/<int:ticket_id>/', views.del_ticket, name='del_ticket'),
    path('tickets/asignar/<int:ticket_id>/', views.asignar_ticket, name='asignar_ticket'),
    path("tickets/cerrar/<int:ticket_id>/", views.cerrar_ticket, name="cerrar_ticket"),
]