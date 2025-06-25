from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView
from .forms import VentaForm, VentaItemFormSet, FiltroVentaForm, Venta

def ventas(request):
    return HttpResponse('Ventas')

class VentaListView(ListView):
    model = Venta
    context_object_name = 'ventas'
    template_name = 'ventas/listado.html'
    paginate_by = 20

    def queryset(self):
        qs = Venta.objects.select_related('usuario').prefetch_related('items__producto')
        user = self.request.user
        if not user.is_superuser:
            qs = qs.filter(usuario=user)

        desde = self.request.GET.get('desde')
        hasta = self.request.GET.get('hasta')

        


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

