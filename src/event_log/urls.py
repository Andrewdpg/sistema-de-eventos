from django.urls import path
from .views import event_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url='e/', permanent=False)),
    path('e/', event_views.actual_events, name='show_events'),
    path('create/', event_views.create_event, name='create_event'),
    path('e/<event_id>/', event_views.event_detail, name='view_event'),
]