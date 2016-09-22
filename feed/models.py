from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

_INTEREST_SOURCES = (
    ('Facebook', 'Facebook'),
    ('Google', 'Google'),
    ('Spotify', 'Spotify'),
    ('Internal', 'Internal')
)


class Request(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    content_type = models.ForeignKey(ContentType, related_name="requested")
    object_id = models.PositiveIntegerField()
    requesting_user = models.ForeignKey(User, related_name="requests")

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'requesting_user')

    def __unicode__(self):
        display_string = "{user} - {content_object}" \
            .format(user=self.user.username, content_object=self.content_object)
        return display_string


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tags'

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'Categories'

    def __unicode__(self):
        return self.name


class Image(models.Model):
    url = models.CharField(max_length=500)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Interest(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200)
    source = models.CharField(max_length=100, choices=_INTEREST_SOURCES)
    images = GenericRelation(Image)
    user = models.ManyToManyField(User)

    class Meta:
        db_table = 'interests'
        unique_together = ('source', 'name')

    def __unicode__(self):
        return self.name


class Event(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    public = models.BooleanField(default=False)

    title = models.CharField(max_length=120)
    location = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    splash_art = models.ImageField(null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)

    requests = GenericRelation(Request, null=True, blank=True)

    user = models.ForeignKey(User, related_name='events')
    attendees = models.ManyToManyField(User, related_name='attending', blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_lat_and_log(self):
        if self.location and (self.latitude is None or self.longitude is None):
            geocoder = Nominatim()
            try:
                new_location = geocoder.geocode(self.location)
                self.location = new_location
                self.latitude = new_location.latitude
                self.longitude = new_location.longitude
            except GeocoderTimedOut:
                print("Error")

    def save(self, *args, **kwargs):
        # self.get_lat_and_log()
        super(Event, self).save(*args, **kwargs)


class Attendance(models.Model):
    user = models.ForeignKey(User, related_name="user_attended")
    event = models.ForeignKey(Event, related_name='event_attendance')
    attended = models.BooleanField(default=False)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username
