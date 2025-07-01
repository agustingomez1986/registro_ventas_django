from django import forms
from django.contrib.auth.models import Group
from .models import Usuarios, Emprendimiento

class ModificarUsuarioForm(forms.ModelForm):
    class Meta:
        model= Usuarios
        fields= ['username', 'first_name', 'email', 'password', 'telefono', 'cuenta_transferencia']
        labels= {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'email': 'Correo electrónico',
            'password': 'Contraseña',
            'telefono': 'Teléfono',
        }
        widgets= {'password': forms.PasswordInput()}

class SignUpForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Grupo",
        required=True
    )

    emprendimiento_existente = forms.ModelChoiceField(
        queryset=Emprendimiento.objects.all(),
        required=False,
        label='Seleccionar emprendimiento existente'
    )

    crear_nuevo_emprendimiento = forms.BooleanField(
        required=False,
        label='Crear nuevo emprendimiento'
    )
    nombre_emprendimiento = forms.CharField(required=False, label='Nombre del nuevo emprendimiento')
    codigo_emprendimiento = forms.CharField(required=False, label='Código del nuevo emprendimiento')


    class Meta:
        model = Usuarios
        fields = ['username', 'first_name', 'email', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'email': 'Correo electrónico',
            'password': 'Contraseña'
        }
        help_texts = {
            'username': 'Requerido. Letras, numeros o @/./+/-/_'
        }
        widgets = {
            'password':forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        crear_nuevo = cleaned_data.get('crear_nuevo_emprendimiento')
        nombre = cleaned_data.get('nombre_emprendimiento')
        codigo = cleaned_data.get('codigo_emprendimiento')
        existente = cleaned_data.get('emprendimiento_existente')

        if crear_nuevo:
            if not nombre or not codigo:
                raise forms.ValidationError('Debes completar nombre y código del nuevo emprendimiento')
        elif not existente:
            raise forms.ValidationError('Debes seleccionar un emprendimiento existente')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.cuenta_transferencia = user.username
        
        if commit:
            user.save()
            grupo = self.cleaned_data['grupo']
            user.groups.add(grupo)

            if self.cleaned_data['crear_nuevo_emprendimiento']:
                emp = Emprendimiento.objects.create(
                    usuario=user,
                    nombre_emprendimiento = self.cleaned_data['nombre_emprendimiento'],
                    codigo_emprendimiento = self.cleaned_data['codigo_emprendimiento'],
                )
            else:
                emp = self.cleaned_data['emprendimiento_existente']
                emp.usuario = user
                emp.save()

        return user

class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model=Emprendimiento
        fields= ['nombre_emprendimiento', 'codigo_emprendimiento']
        labels={
            'nombre_emprendimiento': 'Nombre del emprendimiento',
            'codigo_emprendimiento': 'Código del emprendimiento'
        }

class LoginForm(forms.Form):
    identificador = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')