from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserCreationForm_FirstStage(forms.Form):
    identificacion = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Identificación'})
    )

    email = forms.EmailField(
        max_length=30,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})    
    )

class UserCreationForm_SecondStage(forms.Form):
    c1 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'code_field'})
    )

    c2 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'code_field'})
    )

    c3 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'code_field'})
    )

    c4 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'code_field'})
    )

    c5 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'code_field'})
    )

    c6 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'code_field'})
    )

    def clean(self):
        cleaned_data = super().clean()
        c1 = cleaned_data.get("c1")
        c2 = cleaned_data.get("c2")
        c3 = cleaned_data.get("c3")
        c4 = cleaned_data.get("c4")
        c5 = cleaned_data.get("c5")
        c6 = cleaned_data.get("c6")

        if all([c1, c2, c3, c4, c5, c6]):
            cleaned_data['codigo'] = c1 + c2 + c3 + c4 + c5 + c6
        return cleaned_data

class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('nombre_usuario', 'password1', 'password2')

class CustomLoginForm(forms.Form):
    identificacion = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Identificación'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )

class CustomUserCreationForm(UserCreationForm):
    nombres = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)
    tipo_empleado = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=30)
    # Revisar el tema de hacer CHOICES
    # pais = forms.CharField(max_length=20)
    # departamento = forms.CharField(max_length=20)
    # ciudad = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ('identificacion', 'nombre_usuario','password1', 'password2')

