from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomLoginForm(forms.Form):
    identificacion = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('identificacion', 'nombre_usuario','password1', 'password2')

class UserCreationForm_FirstStage(forms.Form):
    identificacion = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=30)
    codigo = forms.CharField(max_length=6)
