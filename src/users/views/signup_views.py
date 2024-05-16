from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

from ..forms import CustomUserCreationForm
from ..forms import UserCreationForm_FirstStage
from ..mongodb_documents import document_employee

from university.models import Empleados
from ..models import AuthenticationCodes
from pymongo import MongoClient

import secrets, base64
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('DJANGO_HOST'))
db = client['django_db']
collection = db['users_customuser']

# TODO: CAMBIAR LA COLECCION PÂRA LOS DIFERENTES USERS

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

            #TODO
            if empleado.email == email:
                codigo = secrets.token_hex(3)

                codigo_url = secrets.token_hex(3);
                codigo_urlsafe = base64.urlsafe_b64encode(codigo_url.encode()).decode()

                # TODO: Enviar codigo por email
                auth_register = AuthenticationCodes(codigo_url=codigo_urlsafe, code=codigo, empleado_id=empleado.identificacion)
                auth_register.save()

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
    
def signup_validation_view(request, codigo_urlsafe):
    if request.method == 'POST':
        verification_code = request.POST.get('codigo')
        to_redirect = ''
        try:
            auth_code = AuthenticationCodes.objects.get(codigo_url=codigo_urlsafe)

            if auth_code.code == verification_code:
                return redirect('signup_employee', codigo_urlsafe=codigo_urlsafe, codigo_auth=verification_code)
            else:
                # Error de autenticacion el codigo no existe
                pass

            # auth_code.delete()
            return redirect(to_redirect)

        except ObjectDoesNotExist:
            # Error de solicitud, la solicitud no existe
            pass

        pass
    else:
        #TODO: cambiar forms
        form = UserCreationForm_FirstStage()
        return render(request, 'users/signup.html', {'form': form})

def signup_employee(request, codigo_urlsafe, codigo_auth):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            auth_code = AuthenticationCodes.objects.get(codigo_url=codigo_urlsafe)
            auth_code.delete()
            identificacion = form.cleaned_data['identificacion']
            nombre_usuario = form.cleaned_data['nombre_usuario']
            password1 = form.cleaned_data['password1']
            password = make_password(password1)

            document = document_employee(nombre_usuario, password, identificacion)
            collection.insert_one(document)

            return redirect('exito')
    else:
        form = CustomUserCreationForm()
        return render(request, 'users/signup.html', {'form': form})
    
def exito(request):
    return render(request, 'users/exito.html')