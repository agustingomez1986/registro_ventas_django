from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import VentaForm, VentaItemFormSet

def ventas(request):
    return HttpResponse('Ventas')

@login_required
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

