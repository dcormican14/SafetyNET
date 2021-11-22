#Django Libraries
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Our Models
import map_gen.models
from .models import Event, MapVersion, Toggles

# MapMaking
from . import db
from PIL import Image, ImageDraw

# Map Svaing
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

# Create your views here.


def index(request):
    list_of_urls = ['new_event', 'new_event_confirmation', 'edit_new_event_map', 'edit_map']



    return render(request, 'map_gen/index.html', {'list_of_urls': list_of_urls})


def new_event(request):
    return render(request, 'map_gen/new_event.html')


def new_event_confirmation(request):
    event_name = request.POST['event_name_input']
    print(event_name)
    event_type = request.POST['type_input']
    print(event_type)
    event_creator_id = request.POST['creator_id_input']
    print(event_creator_id)
    #
    # if(~(str.length(event_name)<1) | str.length(event_type)<1):
    # figure this out later
    # Redisplay form with Error Message.
    # return render(request, 'map_gen/new_event.html', {'error_message': "Form Incomplete."})
    # else:
    newevent = Event.objects.create(event_name=event_name,
                                 event_type=event_type,
                                 creator_id=event_creator_id,)
    newevent.save()
    print(str(newevent.id))
    dest = "../new_event_map/" + str(newevent.id)
    # raise Exception
    return HttpResponseRedirect(dest)


def edit_new_event_map_v_Old(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event with id [" + event_id + "] not found.")


    c_map = MapVersion.objects.create(creator_id=event.creator_id,
                                      caption_text="",
                                      parent_event=event)

    for x in range(map_gen.models.num_zones):
        Toggles.objects.create(dbNumber=x, parent_map=map)

    img = Image.open('map_gen/minesCampusMapScaled.jpg').convert('RGB')

    d = ImageDraw.Draw(img, mode='RGBA')
    d.polygon(x, fill=(255, 0, 0, 64))

    buildings = dict()
    lots = dict()
    parks = dict()
    streets = dict()
    for (k,v) in db.db["Types"]:
        if v==1:
            print(str(k))
            buildings[k] = {"Name":db.db["Name"][k],
                            "Coordinates":db.db["Coordinates"][k],
                            "Type": db.db["Type"][k],
                            "Toggles": db.db["Toggles"][k],}
        elif v==2:
            print(str(k))
            lots[k] = {"Name": db.db["Name"][k],
                       "Coordinates": db.db["Coordinates"][k],
                       "Type": db.db["Type"][k],
                       "Toggles": db.db["Toggles"][k], }
        elif v==3:
            print(str(k))
            parks[k] = {"Name": db.db["Name"][k],
                        "Coordinates": db.db["Coordinates"][k],
                        "Type": db.db["Type"][k],
                        "Toggles": db.db["Toggles"][k], }
    else:
        print(str(k))
        streets[k] = {"Name": db.db["Name"][k],
                      "Coordinates": db.db["Coordinates"][k],
                      "Type": db.db["Type"][k],
                      "Toggles": db.db["Toggles"][k], }

    with open("db.py", 'r') as f:
            dbstring = f.read()

    print("Here is the dbstring: " + str(dbstring))




    """
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
    """
    return render(request, 'map_gen/edit_map.html', {'image': img,
                                                     'mapversion': c_map,
                                                     'l_buildings': buildings,
                                                     'l_lots': lots,
                                                     'l_parks': parks,
                                                     'l_streets': streets,
                                                     'event_id': event_id})


def new_event_map(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event with id [" + event_id + "] not found.")

    # create the map:
    mapversion = MapVersion.objects.create(
        creator_id=event.creator_id,
        caption_text="",
        parent_event=event,
    )

    # IMAGE MANIPULATION AND SAVING -------------------------------------------
    img = Image.open('map_gen/minesCampusMapScaled.jpg').convert('RGB')

    # x = [(1301, 1297), (1301, 1194), (1361, 1193), (1361, 1297)]
    # d = ImageDraw.Draw(img, mode='RGBA')
    # d.polygon(x, fill=(255, 0, 0, 64))

    savename = "map_" + str(mapversion.pk) + ".jpg"
    buffer = BytesIO()
    img.save(fp=buffer, format='JPEG')
    imgfile = ContentFile(buffer.getvalue())

    mapversion.image.save('savename', InMemoryUploadedFile(
        imgfile,
        None,
        'savename',
        'image/jpeg',
        imgfile.tell,
        None
    ))

    for x in range(map_gen.models.num_zones):
        Toggles.objects.create(dbNumber=x, parent_map=mapversion)

    # Might be more code than necessary ---------------------------------

    l_buildings = {}
    l_lots = {}
    l_parks = {}
    l_streets = {}
    l_areas = {}

    for k in db.db["Type"].keys():
        if db.db["Type"][k] == 1:
            l_buildings[k] = {"Name": db.db["Name"][k],
                            "Coordinates": db.db["Coordinates"][k],
                            "Type": db.db["Type"][k], }
        elif db.db["Type"][k] == 2:
            l_lots[k] = {"Name": db.db["Name"][k],
                       "Coordinates": db.db["Coordinates"][k],
                       "Type": db.db["Type"][k], }
        elif db.db["Type"][k] == 3:
            l_parks[k] = {"Name": db.db["Name"][k],
                        "Coordinates": db.db["Coordinates"][k],
                        "Type": db.db["Type"][k], }
        elif db.db["Type"][k] == 4:
            l_streets[k] = {"Name": db.db["Name"][k],
                          "Coordinates": db.db["Coordinates"][k],
                          "Type": db.db["Type"][k], }
        else:
            l_areas[k] = {"Name": db.db["Name"][k],
                        "Coordinates": db.db["Coordinates"][k],
                        "Type": db.db["Type"][k], }

    # THIS WORKED------------------------------------------------------
    with open("map_gen/db.py", 'r') as f:
        dbstring = f.read()
    data = eval(dbstring[5:])

    names = [(k, v) for k, v in data["Name"].items()]
    names = data["Name"]

    # return statement ------------------------------------------------

    print(event.id)  # double checks the event_map page.

    return render(request, 'map_gen/edit_map.html', {
        'data': data,
        'event': event,
        'image': img,
        'mapversion': mapversion,
        'names': names,
        'l_buildings': l_buildings,
        'l_lots': l_lots,
        'l_parks': l_parks,
        'l_streets': l_streets,
        'l_areas': l_areas,
    })



def edit_map(request):
    return





def edit_map_dev(request):
    event1 = Event.objects.create(
        event_name="What the fuck bro",
        event_type="Pyranna Attack",
        creator_id="Josh Wheadon",)
    event1.save()

    img = Image.open('map_gen/minesCampusMapScaled.jpg').convert('RGB')

    # c_map = MapVersion(
    #     creator_id=event1.creator_id,
    #     caption_text="",
    #     parent_event=event1,
    #     image=img,
    # )

    x = [(1301, 1297), (1301, 1194), (1361, 1193), (1361, 1297)]
    d = ImageDraw.Draw(img, mode='RGBA')
    d.polygon(x, fill=(255, 0, 0, 64))

    c_map = MapVersion.objects.create(
        creator_id=event1.creator_id,
        caption_text="",
        parent_event=event1,
    )

    saveurl = "map_gen/media/map_" + str(c_map.pk) + ".jpg"
    savepath = "map_gen/media"
    savename = "map_" + str(c_map.pk) + ".jpg"

    staticmappath = 'map_gen/minesCampusMapScaled.jpg'

    # THIS FIXED IMAGE SAVING
    buffer = BytesIO()
    img.save(fp=buffer, format='JPEG')
    imgfile = ContentFile(buffer.getvalue())

    c_map.image.save('test456.jpg', InMemoryUploadedFile(
        imgfile,
        None,
        'test456',
        'image/jpeg',
        imgfile.tell,
        None
    ))

    for x in range(map_gen.models.num_zones):
        Toggles.objects.create(dbNumber=x, parent_map=c_map)

    with open("map_gen/db.py", 'r') as f:
        dbstring = f.read()

    data = eval(dbstring[5:])












    buildings = {}
    lots = {}
    parks = {}
    streets = {}
    areas = {}

    for k in data["Type"].keys():
        if data["Type"][k] == 1:
            #print(str(k))
            buildings[k] = {"Name": db.db["Name"][k],
                            "Coordinates": db.db["Coordinates"][k],
                            "Type": db.db["Type"][k], }
        elif db.db["Type"][k] == 2:
            #print(str(k))
            lots[k] = {"Name": db.db["Name"][k],
                       "Coordinates": db.db["Coordinates"][k],
                       "Type": db.db["Type"][k], }
        elif db.db["Type"][k] == 3:
            #print(str(k))
            parks[k] = {"Name": db.db["Name"][k],
                        "Coordinates": db.db["Coordinates"][k],
                        "Type": db.db["Type"][k], }
        elif db.db["Type"][k] == 4:
            #print(str(k))
            streets[k] = {"Name": db.db["Name"][k],
                          "Coordinates": db.db["Coordinates"][k],
                          "Type": db.db["Type"][k], }
        else:
            #print(str(k))
            areas[k] = {"Name": db.db["Name"][k],
                        "Coordinates": db.db["Coordinates"][k],
                        "Type": db.db["Type"][k], }



# THIS WORKED------------------------------------------------------
    names = [(k,v) for k,v in data["Name"].items()]
    names = data["Name"]

    print(names)


            # if data["Type"][k] == 1:
            #     zoneid
            #     # print(str(k))
            #     buildingnames = db.db["Name"][k]
            # elif db.db["Type"][k] == 2:
            #     # print(str(k))
            #     lots[k] = db.db["Name"][k]
            # elif db.db["Type"][k] == 3:
            #     # print(str(k))
            #     parks[k] = db.db["Name"][k]
            # elif db.db["Type"][k] == 4:
            #     # print(str(k))
            #     streets[k] = db.db["Name"][k]
            # else:
            #     # print(str(k))
            #     areas[k] = db.db["Name"][k]



        #print("Here is the dbstring: " + dbstring)
        #str(lots)

    # bkeys = buildings.keys()
    # lkeys = lots.keys()
    # pkeys = parks.keys()
    # skeys = streets.keys()
    # akeys = areas.keys()
    #
    teststring = 'testing pass capability'

    # print(akeys)
    # print(buildings)

    return render (request, 'map_gen/edit_map.html', {
        'data': data,
        'event': event1,
        'teststring': teststring,
        'image': img,
        'mapversion': c_map,
        'names': names,
        'buildings': buildings,
        'l_buildings': buildings,
        'l_lots': lots,
        'l_parks': parks,
        'l_streets': streets,
        'l_areas': areas,
        # 'bkeys' : bkeys,
        # 'lkeys' : lkeys,
        # 'pkeys' : pkeys,
        # 'skeys' : skeys,
        # 'akeys' : akeys,
    })






    """
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
    """
    # return render(request, 'map_gen/edit_map.html', {'image': img,
    #                                                  'c_map': c_map,
    #                                                  'l_buildings': buildings,
    #                                                  'l_lots': lots,
    #                                                  'l_parks': parks,
    #                                                  'l_streets': streets,
    #                                                  'l_areas': areas,
    #                                                  'bkeys' : bkeys,
    #                                                  'lkeys' : lkeys,
    #                                                  'pkeys' : pkeys,
    #                                                  'skeys' : skeys,
    #                                                  'akeys' : akeys,})


