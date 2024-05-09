from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        
        else:
            return render(request, 'users/signup.html', {'form': form})
        
    else:
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})
    
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'users/login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})
    
def signout(request):
    logout(request)
    return redirect('home')