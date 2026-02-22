from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Airports(models.Model):
    icao = models.CharField(max_length=4)
    iata = models.CharField(max_length=3)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    subd = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    elevation = models.CharField(max_length=200)
    lat = models.CharField(max_length=200)
    lon = models.CharField(max_length=200)
    tz = models.CharField(max_length=200)
    lid = models.CharField(max_length=200)

    favorited_by = models.ManyToManyField(
        User,
        related_name="favorite_airports",
        blank=True
    )

    def __str__(self):
        return f"{self.icao} - {self.name}"

    