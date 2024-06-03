from django.urls import path, include
from .views import *

urlpatterns = [
    path('logout/', logout_view, name='signout'),
    path('login/', login_view, name='signin'),
    path('signup/', signup_view, name='signup'),
    path('signup/<codigo_urlsafe>', signup_validation_view, name='signup_auth'),
    path('signup/<codigo_urlsafe>/<codigo_auth>', signup_employee, name='signup_employee'),
    # path('', home_view, name='home'),
    path('', include('pages.urls')),
] 