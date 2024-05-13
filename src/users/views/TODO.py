from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from ..forms import CustomLoginForm, RegisterForm

def home_view(request):
    userInfo = request.user.id
    return render(request, 'pages/home.html', {'userInfo': userInfo})