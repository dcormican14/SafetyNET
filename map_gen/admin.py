from django.contrib import admin

from .models import Event, MapVersion, Toggles

# Register your models here.
admin.site.register(Event)
admin.site.register(MapVersion)
admin.site.register(Toggles)
