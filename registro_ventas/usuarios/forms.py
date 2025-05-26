from django import forms
from .models import Usuarios

class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['first_name', 'email', 'password']
        widget = {
            'passwors':forms.PasswordInput()
        }