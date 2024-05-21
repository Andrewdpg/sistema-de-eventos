from django.urls import path
from .views import endpoints
from .views import *

urlpatterns = [
    path('login/', login_view, name='signin'),
    path('logout/', logout_view, name='signout'),
    path('signup/', signup_view, name='signup'),
    path('signup/<codigo_urlsafe>', signup_validation_view, name='signup_auth'),
    path('signup/<codigo_urlsafe>/<codigo_auth>', signup_employee, name='signup_employee'),
    path('', home_view, name='home'),
    path('exito/', exito, name='exito'),
    
    path('get_departamentos/', endpoints.get_departamentos, name=''),
    path('get_ciudades/', endpoints.get_ciudades, name=''),
]