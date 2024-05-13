from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from ..forms import CustomLoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        password = request.POST.get('password')
        user = authenticate(request, identificacion=identificacion, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            msg = 'Error Login'
            form = CustomLoginForm(request.POST)
            return render(request, 'users/login.html', {'form': form, 'msg': msg})
    else:
        form = CustomLoginForm()
        return render(request, 'users/login.html', {'form': form})