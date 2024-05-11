from django.urls import path
from .views import logout_view, signup_view, login_view_test, home_view

urlpatterns = [
    path('api/login/', login_view_test, name='signin'),
    path('api/logout/', logout_view, name='signout'),
    path('api/signup/', signup_view, name='signup'),
    path('home/', home_view, name='home')
]