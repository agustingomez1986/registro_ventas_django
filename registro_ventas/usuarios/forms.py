from django import forms
from .models import Usuarios

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['username', 'first_name', 'email', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'email': 'Correo electrónico',
            'password': 'Contraseña',
        }
        help_texts = {
            'username': 'Requerido. Letras, numeros o @/./+/-/_'
        }
        widgets = {
            'password':forms.PasswordInput()
        }

class LoginForm(forms.Form):
    identificador = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')