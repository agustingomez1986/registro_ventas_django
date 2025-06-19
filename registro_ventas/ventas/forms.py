from django import forms
from .models import Venta

class VentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None) # extrae 'request' del kwargs
            super().__init__(*args, **kwargs)

            if self.request and self.request.user.is_superuser:
                # Si es superuser, mostrar el campo usuario
                self.fields['usuario'] = forms.ModelChoiceField(
                    queryset=Venta._meta.get_field('usuario').related_model.objects.all(),
                    label='Usuario'
                )

    class Meta:
        model = Venta
        fields = ['fecha']

        
