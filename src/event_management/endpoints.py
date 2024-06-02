from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from connections import universitydb, users, evento
from mongodb_documents import evento_doc, document_user
from datetime import datetime
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

def get_departamentos(request):
    pais_id = request.GET.get('pais_id')

    # Busqueda: Busqeuda de los departamentos de un pais
    with universitydb.cursor() as cursor:
        cursor.execute('SELECT codigo, nombre FROM eventos.departamentos WHERE cod_pais = %s', [pais_id])
        departamentos = cursor.fetchall()
        cursor.close()
    return JsonResponse(departamentos, safe=False)

def get_ciudades(request):
    dpto_id = request.GET.get('dpto_id')

    # Busqueda: Busqueda de las ciudades de un departamento
    with universitydb.cursor() as cursor:
        cursor.execute('SELECT codigo, nombre FROM eventos.ciudades WHERE cod_dpto = %s', [dpto_id])
        ciudades = cursor.fetchall()
        cursor.close()
    return JsonResponse(ciudades, safe=False)

def get_conferencistas(request):
    conferencistas = []
    conferencista_search = request.GET.get('confer_search')

    if (conferencista_search.isdigit()):
        cursor = users.find({'identificacion': {'$regex' : conferencista_search}}, {'_id': 0, 'identificacion': 1, 'nombres': 1, 'apellidos': 1})
    else:
        cursor = users.find({'nombre_completo': {'$regex': conferencista_search}}, {'_id': 0, 'identificacion': 1, 'nombres': 1, 'apellidos': 1})

    for doc in cursor:
        conferencistas.append(doc)

    return JsonResponse(conferencistas, safe=False)

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        titulo = form_data.get('titulo')
        descripcion = form_data.get('descripcion')

        fecha_str = form_data.get('fecha')
        fecha = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M")
        
        lugar = json.loads(form_data.get('lugar'))
        categorias = json.loads(form_data.get('categorias'))
        
        conferencistas = json.loads(form_data.get('conferencistas'))
        facilitadores = json.loads(form_data.get('facilitadores'))
        facultades_org = json.loads(form_data.get('facultades_org'))
        programa_org = form_data.get('programa_org')
        
        if programa_org == '':
            programa_org = None

        evento_to_insert = evento_doc(
            titulo=titulo, 
            descripcion=descripcion, 
            categorias=categorias, 
            fecha=fecha, 
            lugar_datos=lugar, 
            conferencistas=conferencistas, 
            facilitadores=facilitadores, 
            facultades_org=facultades_org, 
            programa_org=programa_org
        )

        evento.insert_one(evento_to_insert)

        # TODO: Aquí agregar el código para guardar los datos en la base de datos
        print('Titulo:', titulo)
        print('Descripcion:', descripcion)
        print('Fecha:', fecha)
        print('Lugar:', lugar)
        print('Categorias:', categorias)
        print('Conferencistas:', conferencistas)
        print('Facilitadores:', facilitadores)
        print('Facultades organizadoras:', facultades_org)
        print('Programa organizador:', programa_org)

        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
@csrf_exempt
def create_normal_user(request):
    if request.method == 'POST':
        # Parsear los datos del formulario a JSON
        form_data = json.loads(request.body)

        # Extraer los datos del formulario
        identificacion = form_data.get('identificacion')
        email = form_data.get('email')
        nombres = form_data.get('nombres')
        apellidos = form_data.get('apellidos')
        nombre_usuario = form_data.get('nombre_usuario')

        password1 = form_data.get('password1')
        password = make_password(password1)

        tipo_relacion = form_data.get('tipo_relacion')
        ciudad = json.loads(form_data.get('ciudad'))

        user_to_insert = document_user(
            identificacion=identificacion, 
            email=email, 
            nombres=nombres, 
            apellidos=apellidos, 
            nombre_usuario=nombre_usuario, 
            password=password, 
            ciudad=ciudad,
            tipo_relacion=tipo_relacion
        )

        users.insert_one(user_to_insert)
        user = authenticate(request, identificacion=identificacion, password=password1)
        login(request, user, backend='users.backends.CustomUserBackend')

        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)