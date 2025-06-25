from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from .forms import VentaForm, VentaItemFormSet, FiltroVentaForm, Venta

def ventas(request):
    return HttpResponse('Ventas')

class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    context_object_name = 'ventas'
    template_name = 'ventas/listado.html'
    paginate_by = 20

    def queryset(self):
        qs = Venta.objects.select_related('usuario').prefetch_related('items__producto')
        user = self.request.user
        # Si usuario no es interno solo verá sus ventas
        if not user.interno:
            qs = qs.filter(usuario=user)

        # Extraemos las fechas del request
        desde = self.request.GET.get('desde')
        hasta = self.request.GET.get('hasta')

        # Convertimos desde y hasta en fechas
        if desde:
            desde_dt = make_aware(datetime.strptime(desde, "%Y-%m-%d"))
            qs = qs.filter(fecha__gte=desde_dt) #fecha mayor o igual que
        if hasta:
            hasta_dt = make_aware(datetime.strptime(hasta, "%Y-%m-%d") + timedelta(days=1))
            qs = qs.filter(fecha__lt=hasta_dt) # fecha menor que

        return qs.order_by('fecha')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_form'] = FiltroVentaForm(self.request.GET)
        return context


@login_required
@user_passes_test(lambda u: u.has_perm('ventas.add_venta'))
def registrar_venta(request):
    if request.method == "POST":
        form = VentaForm(request.POST, request=request)
        formset = VentaItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            venta.total_a_cobrar = 0
            venta.save()

            items = formset.save(commit=False)
            total_item = 0
            for item in items:
                item.venta = venta
                total_item += item.cantidad * item.precio
                item.save()

            venta.total_a_cobrar = total_item
            venta.save()

            messages.success(request, 'Venta registrada exitosamente')
            return redirect('venta')
    else:
        form = VentaForm(request=request)
        formset = VentaItemFormSet()

    return render(request, 'ventas/registrar_venta.html', {'form':form, 'formset':formset,})

