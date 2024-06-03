from django.contrib import admin
from django.urls import path, include
from . import endpoints

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('events/', include('event_log.urls')),

    path('get_departamentos/', endpoints.get_departamentos, name='get_departamentos'),
    path('get_ciudades/', endpoints.get_ciudades, name='get_ciudades'),
    path('get_conferencistas/', endpoints.get_conferencistas, name='get_conferencistas'),
    path('create_event/', endpoints.create_event, name='create_event'),
    path('create_normal_user/', endpoints.create_normal_user, name='create_normal_user'),
]