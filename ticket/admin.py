from django.contrib import admin
from .models import Categoria, EstadoTicket, Ticket, Asignacion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(EstadoTicket)
class EstadoTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

class AsignacionInline(admin.StackedInline):
    model = Asignacion
    extra = 0
    readonly_fields = ('admin', 'desarrollador', 'prioridad', 'fecha_asignacion')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'creador', 'categoria', 'estado', 'desarrollador_asignado', 'prioridad_asignacion', 'created_at')
    list_filter = ('estado', 'categoria', 'created_at')
    search_fields = ('queja', 'creador__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AsignacionInline]

    def desarrollador_asignado(self, obj):
        return obj.asignacion.desarrollador if hasattr(obj, 'asignacion') and obj.asignacion.desarrollador else '-'
    desarrollador_asignado.short_description = 'Desarrollador'

    def prioridad_asignacion(self, obj):
        return obj.asignacion.prioridad if hasattr(obj, 'asignacion') else '-'
    prioridad_asignacion.short_description = 'Prioridad'

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'desarrollador', 'admin', 'prioridad', 'fecha_asignacion')
    list_filter = ('prioridad', 'fecha_asignacion')
    search_fields = ('ticket__id', 'desarrollador__username', 'admin__username')
    ordering = ('-fecha_asignacion',)
