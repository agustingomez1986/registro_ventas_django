from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UsuariosForm

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuariosForm(request.POST)
        if form.is_valid():
            form.save
            return redirect('registro_exitoso')
    else:
        form = UsuariosForm()

    return render(request, 'usuarios/registrar.html', {'form':form})

def usuarios(request):
    return HttpResponse('Inicio de usuarios')

def perfil(request):
    contexto = {'nombre': 'Juan'}
    return render(request, 'usuarios/perfil.html', contexto)