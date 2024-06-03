from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('signin'), 
            reverse('signup'), 
            '/signup/',  # Esto permite cualquier ruta que comience con '/signup/'
            reverse('get_departamentos'),
            reverse('get_ciudades'),
            reverse('get_conferencistas'),
            reverse('create_event'),
            reverse('create_normal_user'),
        ]

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated and not any(url in request.path for url in self.exempt_urls):
            return redirect('signin')
        return response