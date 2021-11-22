

from django.urls import path, include
from . import views

app_name = 'map_gen'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_event/', views.new_event, name='new_event'),
    path('new_event_confirmation/', views.new_event_confirmation, name='new_event_confirmation'),
    path('new_event_map/<int:event_id>/', views.new_event_map, name='new_event_map'),
    path('edit_map/', views.edit_map, name='edit_map'),
    path('edit_map_dev/', views.edit_map_dev, name='edit_map_dev'),
]
