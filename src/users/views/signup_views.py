from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseNotFound

from ..forms import CustomUserCreationForm, UserCreationForm_FirstStage, UserCreationForm_SecondStage, EmployeeCreationForm
from ..mongodb_documents import document_employee, document_user

from university.models import Empleados
from ..models import AuthenticationCodes
from pymongo import MongoClient

import secrets, base64
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('DJANGO_HOST'))
db = client[os.getenv('DJANGO_NAME')]
collection = db[os.getenv('DJANGO_USERS_COLLECTION')]

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return signup_first_stage(request)
    
def signup_first_stage(request):
    form = UserCreationForm_FirstStage()
    
    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        email = request.POST.get('email')
        
        user = collection.find_one({'$or': [{'identificacion': identificacion}, {'email': email}]})

        if user:
            err = "Esta identificacion o email ya se encuentran registrados"
            return render(request, 'users/signup.html', {'form': form, 'err': err})
            
        try:
            empleado = Empleados.objects.get(identificacion=identificacion)

            if empleado.email == email:
                codigo = secrets.token_hex(3)

                codigo_url = secrets.token_hex(3);
                codigo_urlsafe = base64.urlsafe_b64encode(codigo_url.encode()).decode()

                # TODO: Enviar codigo por email
                auth_code = AuthenticationCodes(codigo_url=codigo_urlsafe, code=codigo, empleado_id=empleado.identificacion)
                auth_code.save()

                return redirect('signup_auth', codigo_urlsafe=codigo_urlsafe)
            
            #TODO cambiar al form y la vista que le corresponda
            else:
                err = "La identificacion o el email no coinciden"
                return render(request, 'users/signup.html', {'form': form, 'err': err})
            
        except ObjectDoesNotExist:
            return signup_user(request)

    else:
        return render(request, 'users/signup.html', {'form': form})

# Validar el codigo de autenticacion enviado al correo
def signup_validation_view(request, codigo_urlsafe):  
    try:
        auth_code = AuthenticationCodes.objects.get(codigo_url=codigo_urlsafe)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Page Not Found")

    if request.method == 'POST':
        form = UserCreationForm_SecondStage(request.POST)

        if form.is_valid():
            user_auth_code = form.cleaned_data.get('codigo')
            to_redirect = ''
        else:
            # Error de validacion
            pass

        if auth_code.code == user_auth_code:
            return redirect('signup_employee', codigo_urlsafe=codigo_urlsafe, codigo_auth=user_auth_code)
        else:
            # auth_code.delete()
            err_msg = 'Mensaje de Error'
            # Error de autenticacion el codigo no existe
            pass

        return redirect(to_redirect)

    else:
        form = UserCreationForm_SecondStage()
        return render(request, 'users/signup.html', {'form': form})

def signup_employee(request, codigo_urlsafe, codigo_auth):
    try:
        auth_code = AuthenticationCodes.objects.get(codigo_url=codigo_urlsafe)

        if (auth_code.code != codigo_auth):
            return HttpResponseNotFound("Page Not Found")

        identificacion = auth_code.empleado_id

    except ObjectDoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)

        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            password1 = form.cleaned_data['password1']
            password = make_password(password1)

            document_employee_i = document_employee(nombre_usuario, password, identificacion)
            collection.insert_one(document_employee_i)

            auth_code.delete()
            
            return redirect('exito')
            
    else:
        form = EmployeeCreationForm()
        return render(request, 'users/signup.html', {'form': form})

def signup_user(request):
    form = CustomUserCreationForm(request.POST or None)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        password = make_password(cleaned_data['password1'])
            
        document_user_i = document_user(
            identificacion=cleaned_data['identificacion'],
            nombres=cleaned_data['nombres'],
            apellidos=cleaned_data['apellidos'],
            tipo_empleado=cleaned_data['tipo_empleado'],
            email=cleaned_data['email'],
            pais=cleaned_data['pais'],
            departamento=cleaned_data['departamento'],
            ciudad=cleaned_data['ciudad'],
            nombre_usuario=cleaned_data['nombre_usuario'],
            password=password
        )
        
        collection.insert_one(document_user_i)
    
        return redirect('exito')
    
    else:
        return render(request, 'users/signup.html', {'form': form})

def exito(request):
    return render(request, 'users/exito.html')