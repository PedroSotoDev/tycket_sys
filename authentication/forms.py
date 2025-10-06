from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class RegisterForm(UserCreationForm):
    rol = forms.ChoiceField(
        choices=[
            ("Administrador", "Administrador"),
            ("Desarrollador", "Desarrollador"),
            ("Usuario", "Usuario"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Rol"
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "rol"]
        labels = {
            "username": "Nombre de usuario",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = Group.objects.get(name=self.cleaned_data["rol"])
            user.groups.add(group)
        return user

