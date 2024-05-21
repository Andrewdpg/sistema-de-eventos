from django.http import JsonResponse
from connections import universitydb

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