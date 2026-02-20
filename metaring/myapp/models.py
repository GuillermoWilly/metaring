from django.db import models

# Create your models here.

class TodoItems(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

class Airports(models.Model):
    icao = models.CharField(max_length=4)
    iata = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    subd = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    elevation = models.CharField(max_length=200)
    lat = models.CharField(max_length=200)
    lon = models.CharField(max_length=200)
    tz = models.CharField(max_length=200)
    lid = models.CharField(max_length=200)

    