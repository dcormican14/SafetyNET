from django.shortcuts import render, redirect, get_object_or_404
import pickle
from django.urls import reverse
from . import db

import map_gen.models
from .models import Event, MapVersion, Toggles

# Create your views here.


def index(request):
    list_of_urls = ['new_event', 'new_event_confirmation', 'edit_new_event_map', 'edit_map']

    return render(request, 'map_gen/edit_map.html', {'list_of_urls': list_of_urls})


def new_event(request):
    return render(request, 'map_gen/new_event.html')


def new_event_confirmation(request, event_id):
    event_name = request.POST['event_name_input']
    event_type = request.POST['type_input']
    event_creator_id = request.POST['creator_id_input']
    event_time_created = request.POST['time_created_input']
    #
    # if(~(str.length(event_name)<1) | str.length(event_type)<1):
    # figure this out later
    # Redisplay form with Error Message.
    # return render(request, 'map_gen/new_event.html', {'error_message': "Form Incomplete."})
    # else:
    event = Event.objects.create(event_name=event_name,
                                 event_type=event_type,
                                 creator_id=event_creator_id,)
    return render(request, new_event_confirmation, {'event': event})


def edit_new_event_map(request):
    # event = get_object_or_404(Event, ) # id=event_id)
    event1 = Event.objects.create(event_name="Arbitrary Event",
                                  event_type="Plague",
                                  creator_id="lmoser",)

    map1 = MapVersion.objects.create(creator_id=event1.creator_id,
                                     caption_text="Test PSA Message",
                                     parent_event=event1)

    for x in range(map_gen.models.num_zones):
        Toggles.objects.create(dbNumber=x, parent_map=map1)

    print(type(map1.toggles_set.filter(dbNumber__exact=15).first()))
    print(type(map1.toggles_set.get(dbNumber__exact=15)))
    # tog = map1.toggles_set.get(dbNumber__exact=15)
    tog = map1.toggles_set.get(dbNumber__exact=15)
    tog.toggle = True
    tog.save()

    # tog.toggle = True
    print(map1.toggles_set.get(dbNumber__exact=15).toggle)
    # print(tog)

    print(db.db)

    return render(request, 'map_gen/edit_map.html', {'event': event1, 'map': map1})


def edit_map(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    render(request, 'map_gen/edit_map.html', {'event': event})
