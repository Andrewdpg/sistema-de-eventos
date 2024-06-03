from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login

from ..forms import CustomUserCreationForm, UserCreationForm_FirstStage, UserCreationForm_SecondStage, EmployeeCreationForm
from mongodb_documents import document_user

from ..models import AuthenticationCodes
from connections import universitydb
from pymongo import MongoClient
from users.email_sender import send_email

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
        
        # Busqueda: Se busca un usuario con la identificacion o email ingresados (para evitar duplicados)
        user = collection.find_one({'$or': [{'identificacion': identificacion}, {'email': email}]})

        if user:
            err = "La identificacion o email ya se encuentran registrados"
            return render(request, 'users/signup.html', {'form': form, 'err': err})
            
        # Busqueda: Se busca en la base de datos de la universidad, para ver si el id y el email que se ve van a emplear ya estan en la db.
        cur = universitydb.cursor()
        cur.execute('SELECT identificacion, email FROM eventos.empleados WHERE identificacion = %s', [identificacion])
        empleado = cur.fetchone()
        cur.close()

        if empleado is not None:
            if empleado[1] == email:
                codigo = secrets.token_hex(3)

                codigo_url = secrets.token_hex(3);
                codigo_urlsafe = base64.urlsafe_b64encode(codigo_url.encode()).decode()
                
                auth_code = AuthenticationCodes(codigo_url=codigo_urlsafe, code=codigo, empleado_id=empleado[0])
                auth_code.save()

                send_email(email, codigo)

                return redirect('signup_auth', codigo_urlsafe=codigo_urlsafe)
            
            else:
                err = "La identificacion o email no coinciden"
                return render(request, 'users/signup.html', {'form': form, 'err': err})   
                     
        else:
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

        if auth_code.code == user_auth_code:
            return redirect('signup_employee', codigo_urlsafe=codigo_urlsafe, codigo_auth=user_auth_code)
        else:
            err = 'El codigo ingresado no es valido'
            return render(request, 'users/auth_code.html', {'form': form, 'err': err})

    else:
        form = UserCreationForm_SecondStage()
        return render(request, 'users/auth_code.html', {'form': form})

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

            cur = universitydb.cursor()
            
            cur.execute('SELECT identificacion, email, nombres, apellidos, lugar_nacimiento, tipo_empleado FROM eventos.empleados WHERE identificacion = %s', [identificacion])
            empleado = cur.fetchone()
            
            cur.execute('SELECT nombre, cod_dpto FROM eventos.ciudades WHERE codigo = %s', [empleado[4]])
            ciudad = cur.fetchone()

            cur.execute('SELECT nombre, cod_pais FROM eventos.departamentos WHERE codigo = %s', [ciudad[1]])
            departamento = cur.fetchone()

            cur.execute('SELECT nombre FROM eventos.paises WHERE codigo = %s', [departamento[1]])
            pais = cur.fetchone()
            
            cur.close()

            ciudad_data = {
                'nombre': ciudad[0],
                'departamento': departamento[0],
                'pais': pais[0]
            }

            user_to_insert = document_user(
                identificacion=identificacion,
                email=empleado[1], 
                nombres=empleado[2], 
                apellidos=empleado[3], 
                nombre_usuario=nombre_usuario, 
                password=password, 
                ciudad=ciudad_data,
                tipo_relacion=empleado[5]
            )

            collection.insert_one(user_to_insert)
            auth_code.delete()

            user = authenticate(request, identificacion=identificacion, password=password1)
            login(request, user, backend='users.backends.CustomUserBackend')

            return redirect('home')
            
    else:
        form = EmployeeCreationForm()
        return render(request, 'users/signup_employee.html', {'form': form})

def signup_user(request):
    cur = universitydb.cursor()
    cur.execute('SELECT codigo, nombre FROM eventos.paises')
    paises = cur.fetchall()
    cur.close()

    form = CustomUserCreationForm(request.POST or None)

    return render(request, 'users/signup_user.html', {'form': form, 'paises': paises})