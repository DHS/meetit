from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=200)
    origin = models.CharField(max_lenght=200)

class Calendar(models.Model):
    url = models.URLField(max_length=200)
    user = models.ForeignKey(User, related_name='calendars')

class Event(models.Model):
    user = models.ForeignKey(User, related_name='events')
    calendar = models.ForeignKey(Calendar, related_name='events')
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)

