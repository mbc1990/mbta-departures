from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Departure(models.Model):
    # Last updated (timestamp)
    last_updated = models.DateTimeField()   

    # origin (enum)
    origin = models.CharField(null=False, max_length=128)
    
    # trip number
    # This is a CharField because one of the examples has a trip number like "P109", but I haven't seen the API return that
    trip = models.CharField(null=False, max_length=128)

    # destination (string)
    destination = models.CharField(null=False, max_length=256)

    # scheduled_timed (timestmap)
    scheduled_time = models.DateTimeField(null=False)

    # lateness (interval)
    lateness = models.DurationField(null=False)

    # track (int)
    track = models.IntegerField(null=True)

    # status 
    STATUS_ON_TIME = 1
    STATUS_CANCELLED = 2
    STATUS_ARRIVING = 3
    STATUS_END = 4
    STATUS_NOW_BOARDING = 5
    STATUS_INFO_TO_FOLLOW = 6
    STATUS_ARRIVED = 7
    STATUS_ALL_ABOARD = 8
    STATUS_TBD = 9
    STATUS_DEPARTED = 10
    STATUS_DELAYED = 11
    STATUS_LATE = 12
    STATUS_HOLD = 13
    STATUS_CHOICES = (
        (STATUS_ON_TIME, "On Time"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_ARRIVING, "Arriving"),
        (STATUS_END, "End"),
        (STATUS_NOW_BOARDING, "Now Boarding"),
        (STATUS_INFO_TO_FOLLOW, "Info to Follow"),
        (STATUS_ARRIVED, "Arrived"),
        (STATUS_ALL_ABOARD, "All Aboard"),
        (STATUS_TBD, "TBD"),
        (STATUS_DEPARTED, "Departed"),
        (STATUS_DELAYED, "Delayed"),
        (STATUS_LATE, "Late"),
        (STATUS_HOLD, "Hold"),
    )
    status = models.IntegerField(null=False, choices=STATUS_CHOICES)
