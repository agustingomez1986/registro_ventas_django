from django import forms
from .models import Usuarios

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['username', 'first_name', 'email', 'password']
        widgets = {
            'password':forms.PasswordInput()
        }

class LoginForm(forms.Form):
    identificador = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')