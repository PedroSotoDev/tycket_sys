from django.db import models
from django.contrib.auth.models import User

# Tablas nomencladoras
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class EstadoTicket(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.nombre


# Tabla Ticket
class Ticket(models.Model):
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='tickets')
    estado = models.ForeignKey(EstadoTicket, on_delete=models.PROTECT, related_name='tickets')
    queja = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket #{self.id} - {self.categoria} - {self.estado}"


# Tabla de asignación admin-dev-ticket
class Asignacion(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='asignacion')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')
    desarrollador = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='tickets_recibidos')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    prioridad = models.CharField(
        max_length=10,
        choices=[('baja','Baja'),('media','Media'),('alta','Alta'),('critica','Crítica')],
        default='media'
    )

    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"Ticket #{self.ticket.id} asignado a {self.desarrollador} por {self.admin}"
