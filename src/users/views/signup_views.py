from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from ..forms import CustomUserCreationForm as UserCreationForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

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
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})