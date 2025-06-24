from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignUpForm, LoginForm

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administrador').exists())
def registrar_usuario(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente')
            return redirect('signup')
    else:
        form = SignUpForm()

    return render(request, 'usuarios/signup.html', {'form':form})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identificador = form.cleaned_data['identificador']
            password = form.cleaned_data['password']
            user = authenticate(request, username=identificador, password=password)
            if user is not None:
                login(request, user)
                return redirect('perfil')
            else:
                form.add_error(None, 'Credenciales invalidas')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form':form})

@login_required(login_url='login')
def perfil(request):
    return render(request, 'usuarios/perfil.html')