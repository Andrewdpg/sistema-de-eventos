from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from ..collections import evento, categorias


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
    # Busqueda: Se hace una busqueda de un evento en especifico por su _id

    event = evento.find_one({'_id' : ObjectId(event_id)})

    return render(request, 'event_log/event_detail.html', {'event': event})
