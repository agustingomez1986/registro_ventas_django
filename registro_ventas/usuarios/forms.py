from django import forms
from django.contrib.auth.models import Group
from .models import Usuarios

class SignUpForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Grupo",
        required=True
    )

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            grupo = self.cleaned_data['grupo']
            user.groups.add(grupo)
        return user


class LoginForm(forms.Form):
    identificador = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')