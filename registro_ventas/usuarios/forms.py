from django import forms
from .models import Usuarios

class UsuariosRegForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['username', 'first_name', 'email', 'password']
        widgets = {
            'password':forms.PasswordInput()
        }

class LoginForm(forms.Form):
    identificador = forms.CharField(label='Email o Celular')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')