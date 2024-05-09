from django.urls import path
from users import views
from pages import views as pages_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('', pages_views.home, name='home'),
]