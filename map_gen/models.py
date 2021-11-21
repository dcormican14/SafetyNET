from django.db import models
from django.utils import timezone

# Create your models here.
num_zones = 115


class Event(models.Model):
    creator_id = models.CharField("Event creator's CSM username", max_length=31,)
    event_type = models.CharField("Nature of this event, from list. May be enum later.", max_length=31)
    time_created = models.DateTimeField('Date and time of event creation', auto_now_add=True)
    event_name = models.CharField("Event/incident name", max_length=128,)

    def __str__(self):
        return self.event_name + \
               " IS A " + self.event_type \
               + " CREATED BY " + self.creator_id \
               + " ON " + str(self.time_created) \
               + " WITH ID " + str(self.id)

    def was_created_recently(self):
        return self.time_created >= timezone.now() - timezone.timedelta(days=10)


class MapVersion(models.Model):
    creator_id = models.CharField("Event creator's CSM username", max_length=31,)
    time_created = models.DateTimeField('Date and time of new version creation', auto_now_add=True)
    buffer_radius = models.IntegerField('Size in pixels of safety buffer zone', default=0)
    is_airborne = models.BooleanField('Indicates airborne chemical threat.', default=False)
    # shape_toggles = models.BinaryField(bytearray(15), max_length=15,)
    caption_text = models.CharField(max_length=1024)
    parent_event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)


class Toggles(models.Model):
    toggle = models.BooleanField(default=False)
    dbNumber = models.IntegerField(default=-1)
    parent_map = models.ForeignKey(MapVersion, on_delete=models.CASCADE, default=1)


