from django.apps import AppConfig
from django.db.models.signals import post_migrate

class TicketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticket'

    def ready(self):
        post_migrate.connect(create_initial_data, sender=self)


def create_initial_data(sender, **kwargs):

    from .models import Categoria, EstadoTicket

    categorias = ["Error", "Mejora", "Nueva funcionalidad"]
    for nombre in categorias:
        Categoria.objects.get_or_create(nombre=nombre)

    estados = ["Abierto", "En proceso", "En revisión", "Cerrado"]
    for nombre in estados:
        EstadoTicket.objects.get_or_create(nombre=nombre)

