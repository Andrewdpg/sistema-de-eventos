from django.contrib import admin
from django.urls import path, include
from . import endpoints

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('events/', include('event_log.urls')),

    
    path('get_departamentos/', endpoints.get_departamentos, name=''),
    path('get_ciudades/', endpoints.get_ciudades, name=''),
    path('get_conferencistas/', endpoints.get_conferencistas, name=''),
    path('create_event/', endpoints.create_event, name=''),
    path('create_normal_user/', endpoints.create_normal_user, name=''),
]