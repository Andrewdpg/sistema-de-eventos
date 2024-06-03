from django.urls import path
from .views import *

urlpatterns = [
    # path('', home_view, name='home'),
    path('', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
]