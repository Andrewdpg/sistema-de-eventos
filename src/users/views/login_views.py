from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from ..forms import CustomLoginForm
from django.db import DatabaseError

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        password = request.POST.get('password')
        user = authenticate(request, identificacion=identificacion, password=password)

        if user is not None:
            try:
                login(request, user, backend='users.backends.CustomUserBackend')
                return redirect('home')
            except DatabaseError as e:
                print(user.identificacion)
                print(user.password)
                print("Aqui ocurrio el error: " + str(e))
        else:
            msg = 'Error Login'
            form = CustomLoginForm(request.POST)
            return render(request, 'users/login.html', {'form': form, 'msg': msg})
    else:
        form = CustomLoginForm()
        return render(request, 'users/login.html', {'form': form})