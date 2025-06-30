from collections import defaultdict
from itertools import groupby
from operator import attrgetter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from .forms import VentaForm, VentaItemFormSet, FiltroVentaForm, Venta

def defaultdict_to_dict(d):
        if isinstance(d, defaultdict):
            d = {k: defaultdict_to_dict(v) for k, v in d.items()}
        return d

# CBV Class Based Views

class VentaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Venta
    context_object_name = 'ventas'
    template_name = 'ventas/listado_ventas.html'
    paginate_by = 20
    permission_required = 'ventas.view_venta'

    def get_queryset(self):
        qs = Venta.objects.select_related('usuario').prefetch_related('items')
        user = self.request.user
        # Si usuario no es administrador o vendedor solo verá sus ventas
        if not user.groups.filter(name__in=['administrador', 'vendedor']).exists():
            cod_emprendimiento = user.emprendimiento.values_list('codigo_emprendimiento', flat=True)
            qs = qs.filter(items__codigo_emprendimiento__in=cod_emprendimiento).distinct()

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
        filtro_form = FiltroVentaForm(self.request.GET)
        ventas = self.get_queryset()

        agrupado = defaultdict(lambda:defaultdict(lambda: defaultdict(list)))
        for venta in ventas:
            fecha_str = venta.fecha.strftime("%d/%m/%Y")
            turno = venta.get_turno_display()
            usuario = venta.usuario.get_full_name()
            agrupado[fecha_str][turno][usuario].append(venta)

        context['ventas_agrupadas'] = defaultdict_to_dict(agrupado)
        context['filtro_form'] = filtro_form
        return context

# FBV Function Based Views

@login_required
@user_passes_test(lambda u: u.has_perm('ventas.add_venta'))
def registrar_venta(request):
    if request.method == "POST":
        form = VentaForm(request.POST, request=request)
        formset = VentaItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            venta = form.save(commit=False)
            if request.user.groups.filter(name='administrador').exists():
                venta.usuario = form.cleaned_data['usuario']
            else:
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

