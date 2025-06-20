from django import forms
from django.forms import inlineformset_factory
from .models import Venta, VentaItem

class VentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) # extrae 'request' del kwargs
        super().__init__(*args, **kwargs)

        if self.request and self.request.user.is_superuser:
            # Si es superuser, mostrar el campo usuario
            self.fields['usuario'] = forms.ModelChoiceField(
                queryset=Venta._meta.get_field('usuario').related_model.objects.all(),
                label='Usuario',
                initial=self.request.user,
            )
            self.fields = {'usuario': self.fields['usuario'], **self.fields}

    class Meta:
        model = Venta
        fields = ['fecha', 'turno', 'metodo_pago', 'cuenta_transferencia', 'total_cobrado']
        labels = {
            'fecha': 'Fecha',
            'turno': 'Turno',
            'metodo_pago': 'Método de pago',
            'cuenta_transferencia': 'Cuenta de transferencia',
            'total_cobrado': 'Total cobrado'

        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type':'date'}),
        }

VentaItemFormSet = inlineformset_factory(
    Venta,
    VentaItem,
    fields=['nombre', 'cantidad', 'precio', 'codigo_hacedor', 'codigo_producto'],
    extra=1, # cuántos formularios vacíos mostrar
    can_delete=True
)