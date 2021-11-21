

from django.urls import path, include
from . import views

urlpatterns = [
    path('new_event/', views.new_event, name='new_event'),
    path('new_event_confirmation/', views.new_event_confirmation, name='new_event_confirmation'),
    path('edit_new_event_map/', views.edit_new_event_map, name='edit_new_event_map'),
    path('edit_map/', views.edit_map, name='edit_map'),
]
