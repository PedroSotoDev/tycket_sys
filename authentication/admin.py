from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Primero quitamos el UserAdmin original
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_role', 'is_active', 'is_staff')
    list_filter = ('groups', 'is_staff', 'is_active')

    def get_role(self, obj):
        """
        Muestra el nombre del grupo (rol) principal del usuario.
        Si tiene varios, los une con comas.
        """
        return ", ".join([group.name for group in obj.groups.all()]) or "Sin rol"
    get_role.short_description = 'Rol'