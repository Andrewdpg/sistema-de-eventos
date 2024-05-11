from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .Loginform import LoginForm, RegisterForm

def login_view_test(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            msg = 'Error Login'
            form = LoginForm(request.POST)
            return render(request, 'users/login.html', {'form': form, 'msg': msg})
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

def home_view(request):
    return render(request, 'pages/home.html')

def logout_view(request):
    logout(request)
    return redirect('home')
    
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        
        else:
            return render(request, 'users/signup.html', {'form': form})
        
    else:
        form = RegisterForm()
        return render(request, 'users/signup.html', {'form': form})