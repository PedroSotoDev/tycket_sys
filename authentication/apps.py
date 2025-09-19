from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_roles(sender, **kwargs):
    
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from ticket.models import Ticket

    roles = ["Administrador", "Desarrollador", "Usuario"]
    for role in roles:
        Group.objects.get_or_create(name=role)

    content_type = ContentType.objects.get_for_model(Ticket)
    permisos = Permission.objects.filter(content_type=content_type)

    # admin: todos los permisos
    admin_group = Group.objects.get(name="Administrador")
    admin_group.permissions.add(*permisos)

    # dev: ver y cambiar
    dev_group = Group.objects.get(name="Desarrollador")
    dev_perms = permisos.filter(codename__in=["view_ticket", "change_ticket"])
    dev_group.permissions.add(*dev_perms)

    # user: ver y crear
    user_group = Group.objects.get(name="Usuario")
    user_perms = permisos.filter(codename__in=["view_ticket", "add_ticket"])
    user_group.permissions.add(*user_perms)


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"

    def ready(self):
        post_migrate.connect(create_roles, sender=self)

