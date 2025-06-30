from django import forms
from django.forms import inlineformset_factory
from .models import Venta, VentaItem
from usuarios.models import Usuarios, Emprendimiento

class VentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) # extrae 'request' del kwargs
        super().__init__(*args, **kwargs)

        # Si es administrador, mostrar el campo usuario
        if self.request and self.request.user.groups.filter(name='administrador').exists():
            self.fields['usuario'] = forms.ModelChoiceField(
                queryset=Venta._meta.get_field('usuario').related_model.objects.all(),
                label='Usuario',
                initial=self.request.user,
            )
            self.fields = {'usuario': self.fields['usuario'], **self.fields}

        cuentas = [(cuenta, cuenta) for cuenta in Usuarios.objects
                   .exclude(cuenta_transferencia__isnull = True)
                   .exclude(cuenta_transferencia='')
                   .values_list('cuenta_transferencia', flat = True)
                   .distinct().order_by('cuenta_transferencia')]
        
        self.fields['cuenta_transferencia'] = forms.ChoiceField(
            choices=[('', '--------')] + cuentas,
            label='Cuenta Transferencia',
            required=False,
        )

    class Meta:
        model = Venta
        fields = ['fecha', 'turno', 'metodo_pago', 'total_a_cobrar', 'total_cobrado']
        labels = {
            'fecha': 'Fecha',
            'turno': 'Turno',
            'metodo_pago': 'Método de pago',
            'total_a_cobrar': 'Total a cobrar',
            'total_cobrado': 'Total cobrado'
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type':'date'}),
        }

class VentaItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['codigo_emprendimiento'] = forms.ModelChoiceField(
            queryset=Emprendimiento.objects.all().order_by('codigo_emprendimiento'),
            label='Código Emprendimiento',
        )

        self.fields = {'codigo_emprendimiento': self.fields['codigo_emprendimiento'], **self.fields}

    class Meta:
        model: VentaItem
        fields=['producto', 'cantidad', 'precio', 'codigo_producto']
        labels={
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio': 'Precio unitario',
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
