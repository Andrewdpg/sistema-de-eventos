from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomLoginForm(forms.Form):
    identificacion = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['identificacion', 'tipo_relacion', 'nombre_usuario', 'email', 'first_name', 'last_name', 'ciudad']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.identificacion = self.cleaned_data['identificacion']
        user.tipo_relacion = self.cleaned_data['tipo_relacion']
        user.nombre_usuario = self.cleaned_data['nombre_usuario']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.ciudad = self.cleaned_data['ciudad']
        if commit:
            user.save()
        return user
    
class UserCreationForm_FirstStage(forms.Form):
    identificacion = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=30)
    codigo = forms.CharField(max_length=6)
