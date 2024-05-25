from django.urls import path
from .views import event_views

urlpatterns = [
    path('', event_views.actual_events, name='view_events'),
    path('create/', event_views.create_event, name='create_event'),
    path('r/<event_id>', event_views.event_detail, name='view_event'),
]