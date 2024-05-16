from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

from ..forms import CustomUserCreationForm, UserCreationForm_FirstStage, UserCreationForm_SecondStage, EmployeeCreationForm
from ..mongodb_documents import document_employee

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
    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        email = request.POST.get('email')
        
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
                error = "La identificacion o el email no coinciden"
                return render(request, 'users/signup.html', {'error': error})
            
        except ObjectDoesNotExist:
            #TODO: aqui iria el caso de que no pertenesca a la DB de universidad
            pass

        # acaba de enviar la id y el email
        # !saber si este usuario esta en la base
        # buscar por id, si esta, buscar si el email coincide
        # si coincide, crear un temporal codigo, guardarlo temporalmente en la DB (mirar como hacer este codigo temporal) y enviarlo por email
    else:
        #TODO: cambiar forms
        form = UserCreationForm_FirstStage()
        return render(request, 'users/signup.html', {'form': form})

# Validar el codigo de autenticacion enviado al correo
def signup_validation_view(request, codigo_urlsafe):  
    if request.method == 'POST':
        form = UserCreationForm_SecondStage(request.POST)
        err_msg = ''

        if form.is_valid():
            pass
        else:
            err_msg = 'Mensaje de Error'
            return render(request, 'users/signup.html', {'form': form, 'err_msg': err_msg})

        user_auth_code = form.cleaned_data.get('codigo')
        to_redirect = ''
        try:
            auth_code = AuthenticationCodes.objects.get(codigo_url=codigo_urlsafe)

            if auth_code.code == user_auth_code:
                return redirect('signup_employee', codigo_urlsafe=codigo_urlsafe, codigo_auth=user_auth_code)
            else:
                # auth_code.delete()
                err_msg = 'Mensaje de Error'
                # Error de autenticacion el codigo no existe
                pass

            
            return redirect(to_redirect)

        except ObjectDoesNotExist:
            # Error de solicitud, la solicitud no existe
            pass

        pass
    else:
        form = UserCreationForm_SecondStage()
        return render(request, 'users/signup.html', {'form': form})

def signup_employee(request, codigo_urlsafe, codigo_auth):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            auth_code = AuthenticationCodes.objects.get(codigo_url=codigo_urlsafe)
            identificacion = auth_code.empleado_id

            if (auth_code.code== codigo_auth):

                auth_code.delete()

                nombre_usuario = form.cleaned_data['nombre_usuario']
                password1 = form.cleaned_data['password1']
                password = make_password(password1)

                document_employe = document_employee(nombre_usuario, password, identificacion)
                collection.insert_one(document_employe)

                return redirect('exito')
            
            else:
                # Intento de falsificacion rey, salga de ahi
                pass

    else:
        form = EmployeeCreationForm()
        return render(request, 'users/signup.html', {'form': form})
    
def exito(request):
    return render(request, 'users/exito.html')