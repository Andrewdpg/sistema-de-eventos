from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from connections import universitydb, evento, users
from mongodb_documents import comentario_doc

from datetime import datetime

def all_events(request):
    # Busqueda: Se hace una busqueda de todos los eventos
    events = evento.find()

    return render(request, 'event_log/all_events.html', {'events': events})

def actual_events(request):
    # Busqueda: Se hace una busqueda de todos los eventos que no hayan pasado del dia actual.

    today = datetime.today()
    today = datetime(today.year, today.month, today.day)

    events = evento.find({"fecha": {'$gte': today}})

    return render(request, 'event_log/all_events.html', {'events': events})

def event_detail(request, event_id):
    usuario = request.user.identificacion

    if request.method == 'POST':

        if 'submit-comment' in request.POST:
            comentario = request.POST.get('comentario')
            fecha = datetime.today()
            fecha = datetime(fecha.year, fecha.month, fecha.day)

            comentario_to_i = comentario_doc(
                comentario=comentario, 
                fecha=fecha, 
                usuario=usuario
            )
            
            # Insert: Ser inserta un comentario del usuario en un evento en especifico
            evento.update_one({'_id': ObjectId(event_id)}, {'$push': {'comentarios': comentario_to_i}})
            return redirect('view_event', event_id=event_id)
        
        elif 'submit-attendance' in request.POST:
            asistente = evento.find_one({'_id': ObjectId(event_id), 'asistentes.identificacion': {'$in': [usuario]}})

            if asistente is not None:
                evento.update_one(
                    {'_id': ObjectId(event_id), 'asistentes.identificacion': usuario},
                    {'$set': {'asistentes.$.estado_asistencia': 'PRESENCIAL'}})

            return redirect('view_event', event_id=event_id)
        
        elif 'submit-register' in request.POST:
            asistente = evento.find_one({'_id': ObjectId(event_id), 'asistentes.identificacion': {'$in': [usuario]}})

            if asistente is None:
                info_user = {
                    'identificacion': usuario,
                    'estado_asistencia': 'INSCRITO' 
                }

                evento.update_one({'_id': ObjectId(event_id)}, {'$push': {'asistentes': info_user}})
            
            return redirect('view_event', event_id=event_id)
        
    else: 
        # Busqueda: Se hace una busqueda de un evento en especifico por su _id
        event = evento.find_one({'_id' : ObjectId(event_id)})
        return render(request, 'event_log/event_detail.html', {'event': event})

def create_event(request):
    cur = universitydb.cursor()

    cur.execute('SELECT codigo, nombre FROM eventos.programas')
    programas = cur.fetchall()

    cur.execute('SELECT codigo, nombre FROM eventos.paises')
    paises = cur.fetchall()

    cur.execute('SELECT codigo, nombre FROM eventos.facultades')
    facultades = cur.fetchall()
    
    cur.close()
        
    return render(request, 'event_log/create_event.html', {'programas': programas, 'paises': paises, 'facultades': facultades})