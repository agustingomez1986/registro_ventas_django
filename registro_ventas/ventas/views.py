from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import VentaForm

def ventas(request):
    return HttpResponse('Ventas')

@login_required
def registrar_venta(request):
    if request.method == "POST":
        form = VentaForm(request.POST, request=request)
        if form.is_valid():
            venta = form.save(commit=False)

            if not request.user.is_superuser:
                venta.usuario = request.user

            venta.save()

            messages.success(request, 'Venta registrada exitosamente')
            return redirect('venta')
    else:
        form = VentaForm()

    return render(request, 'ventas/registrar_venta.html', {'form':form})

