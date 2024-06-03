from django.shortcuts import render

def home_view(request):
    userInfo = request.user.__dict__
    return render(request, 'pages/home.html', {'userInfo': userInfo})