from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from connections import universitydb

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_usuario'].widget.attrs.update({'placeholder': 'Nombre de Usuario'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmar Contraseña'})

class CustomLoginForm(forms.Form):
    identificacion = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Identificación'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )

class CustomUserCreationForm(UserCreationForm):
    nombres = forms.CharField(
        max_length=30,
         widget=forms.TextInput(attrs={'placeholder': 'nombre(s)'})
    )

    apellidos = forms.CharField(
        max_length=30,
         widget=forms.TextInput(attrs={'placeholder': 'apelldo(s)'})
    )

    tipo_empleado = forms.ChoiceField()

    email = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'email'})
    )
    # Revisar el tema de hacer CHOICES
    # pais = forms.CharField(max_length=20)
    # departamento = forms.CharField(max_length=20)
    # ciudad = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ('identificacion', 'nombre_usuario','password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        with universitydb.cursor() as cursor:
            cursor.execute('SELECT nombre, nombre FROM eventos.tipos_empleado')
            choices = cursor.fetchall()
        self.fields['tipo_empleado'].choices = choices
        self.fields['identificacion'].widget.attrs.update({'placeholder': 'identificacion', 'id': 'identificacion'})
        self.fields['email'].widget.attrs.update({'placeholder': 'email', 'id': 'email'})
        self.fields['nombres'].widget.attrs.update({'placeholder': 'nombre(s)', 'id': 'nombres'})
        self.fields['apellidos'].widget.attrs.update({'placeholder': 'apellido(s)', 'id': 'apellidos'})
        self.fields['tipo_empleado'].widget.attrs.update({'id': 'tipo_relacion'})
        self.fields['nombre_usuario'].widget.attrs.update({'placeholder': 'nombre de usuario', 'id': 'nombre_usuario'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'contraseña', 'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'confirmar contraseña', 'id': 'password2'})
