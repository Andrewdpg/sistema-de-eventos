from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def home_view(request):
    userInfo = request.user.__dict__
    return render(request, 'pages/home.html', {'userInfo': userInfo})