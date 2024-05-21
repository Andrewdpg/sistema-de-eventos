from django.urls import path
from .views import event_views

urlpatterns = [
    path('', event_views.actual_events, name='view_events'),
    path('<event_id>', event_views.event_detail, name='view_event'),
]