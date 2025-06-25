from django import forms
from django.forms import inlineformset_factory
from .models import Venta, VentaItem

class VentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) # extrae 'request' del kwargs
        super().__init__(*args, **kwargs)

        if self.request and self.request.user.groups.filter(name__in='administrador').exists():
            # Si es superuser, mostrar el campo usuario
            self.fields['usuario'] = forms.ModelChoiceField(
                queryset=Venta._meta.get_field('usuario').related_model.objects.all(),
                label='Usuario',
                initial=self.request.user,
            )
            self.fields = {'usuario': self.fields['usuario'], **self.fields}

    class Meta:
        model = Venta
        fields = ['fecha', 'turno', 'metodo_pago', 'cuenta_transferencia', 'total_a_cobrar', 'total_cobrado']
        labels = {
            'fecha': 'Fecha',
            'turno': 'Turno',
            'metodo_pago': 'Método de pago',
            'cuenta_transferencia': 'Cuenta de transferencia',
            'total_a_cobrar': 'Total a cobrar',
            'total_cobrado': 'Total cobrado'
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type':'date'}),
        }

class VentaItemForm(forms.ModelForm):
    class Meta:
        model: VentaItem
        fields=['nombre', 'cantidad', 'precio', 'codigo_hacedor', 'codigo_producto']
        labels={
            'nombre': 'Producto',
            'cantidad': 'Cantidad',
            'precio': 'Precio unitario',
            'codigo_hacedor': 'Hacedor',
            'codigo_producto': 'Código de producto'
        }



VentaItemFormSet = inlineformset_factory(
    Venta,
    VentaItem,
    form=VentaItemForm,
    extra=3, # cuántos formularios vacíos mostrar
    can_delete=True
)

class FiltroVentaForm(forms.Form):
    desde = forms.DateField(
        required=False,
        label='Desde',
        widget=forms.DateInput(attrs={'type':'date'})
    )
    hasta = forms.DateField(
        required=False,
        label='Hasta',
        widget=forms.DateInput(attrs={'type':'date'})
    )
