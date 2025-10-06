from django import forms
from .models import Ticket, EstadoTicket, Categoria
from django.contrib.auth.models import User

PRIORIDAD_CHOICES = (
    (1, 'Baja'),
    (2, 'Media'),
    (3, 'Alta'),
    (4, 'critica'),
)

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['queja', 'categoria']
        widgets = {
            'queja': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,                
                'placeholder': 'Describe tu ticket aquí...'
            }),
            'categoria': forms.Select(attrs={'class': 'form-select'})
        }

class FilterTicketForm(forms.Form):
    estado = forms.ModelChoiceField(
        queryset=EstadoTicket.objects.all(), 
        required=False, 
        label="Estado",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        label="Categoría",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    desarrollador = forms.ModelChoiceField(
        queryset=User.objects.filter(tickets_recibidos__isnull=False).distinct(),
        required=False,
        label="Desarrollador",
        widget=forms.Select(attrs={"class": "form-select"})
    )

class EditTicketForm(forms.ModelForm):
    estado = forms.ModelChoiceField(
        queryset=EstadoTicket.objects.all(),
        required=True,
        label="Estado",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    desarrollador = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False),
        required=False,
        label="Desarrollador",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    prioridad = forms.ChoiceField(
        choices=PRIORIDAD_CHOICES,
        required=True,
        label="Prioridad",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Ticket
        fields = ['estado', 'desarrollador', 'prioridad']