from datetime import datetime
from bson import ObjectId
from django.shortcuts import render
from connections import users, evento
from event_management.endpoints import recommend_events, validate_permissions


def home_view(request):
    userInfo = request.user.__dict__
    return render(request, 'pages/home.html', {'userInfo': userInfo, 'can_create_event': validate_permissions(request.user.identificacion, 'crear_evento')})

def profile_view(request):
    userInfo = users.find_one({'identificacion': request.user.identificacion})
    # Obtener los ultimos 4 eventos a los que asistio
    attended_events = evento.find({"asistentes": {"$elemMatch": {"identificacion": userInfo['identificacion'], "estado_asistencia": "PRESENCIAL"}}}).limit(4)

    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    
    puntajes = None
    if 'recomendaciones' in userInfo:
        puntajes = userInfo['recomendaciones']['porcentajes']

        # Obtener los 4 mejores puntajes de eventos en "porcentajes"
        puntajes = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)[:4]

        # obtener la informacion de los eventos con los id de los puntajes
        best_events = evento.find({"_id": {"$in": [ObjectId(i[0]) for i in puntajes]}})
    else:
        best_events = evento.find({"fecha": {"$gte": today}})

    # Obtener los 4 eventos más recomendados
    best_events = recommend_events(request, list(best_events), today)
    
    best_events = sorted(best_events, key=lambda x: x['porcentaje'], reverse=True)
    best_events = best_events[:4]

    return render(request, 'pages/profile.html', {'userInfo': userInfo, 'attended_events': attended_events, 'best_events': best_events})
