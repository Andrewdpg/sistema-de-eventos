from django.urls import path
from .views import logout_view, signup_view, login_view

urlpatterns = [
    path('login/', login_view, name='signin'),
    path('logout/', logout_view, name='signout'),
    path('signup/', signup_view, name='signup'),
    path('', home_view, name='home')
]