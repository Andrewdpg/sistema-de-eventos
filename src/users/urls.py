from django.urls import path
from users import views

urlpatterns = [
    path('', views.signup, name='signup'),
]