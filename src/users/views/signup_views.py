from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseNotFound

from ..forms import CustomUserCreationForm, UserCreationForm_FirstStage, UserCreationForm_SecondStage, EmployeeCreationForm
from ..mongodb_documents import document_employee, document_user

from ..models import AuthenticationCodes
from connections import universitydb
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

        if empleado is None:
            return signup_user(request)
        else:
    
            if empleado[0][1] == email:
                codigo = secrets.token_hex(3)

                codigo_url = secrets.token_hex(3);
                codigo_urlsafe = base64.urlsafe_b64encode(codigo_url.encode()).decode()

                # TODO: Enviar codigo por email
                auth_code = AuthenticationCodes(codigo_url=codigo_urlsafe, code=codigo, empleado_id=empleado.identificacion)
                auth_code.save()

                return redirect('signup_auth', codigo_urlsafe=codigo_urlsafe)
            
            else:
                err = "La identificacion o email no coinciden"
                return render(request, 'users/signup.html', {'form': form, 'err': err})            

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
    cur = universitydb.cursor()
    cur.execute('SELECT codigo, nombre FROM eventos.paises')
    paises = cur.fetchall()
    cur.close()

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
            pais=request.POST.get('paises'),
            departamento=request.POST.get('departamentos'),
            ciudad=request.POST.get('ciudades'),
            nombre_usuario=cleaned_data['nombre_usuario'],
            password=password
        )
        
        collection.insert_one(document_user_i)
    
        return redirect('exito')
    
    else:
        return render(request, 'users/signup_user.html', {'form': form, 'paises': paises})

def exito(request):
    return render(request, 'users/exito.html')