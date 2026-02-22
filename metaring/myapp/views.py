from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import *
from .utils import get_metar_from_icao


def home(request):
    return render(request, "home.html")

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(request, "registration/register.html", {
        "form": form
    })


def airport_detail(request, icao):
    airport = get_object_or_404(Airports, icao=icao.upper())
    metar_data = get_metar_from_icao(icao.upper())

    return render(request, "airport_detail.html", {
        "airport": airport,
        "metar": metar_data
    })

@login_required
def toggle_favorite(request, icao):

    airport = get_object_or_404(Airports, icao=icao.upper())

    if request.user in airport.favorited_by.all():
        airport.favorited_by.remove(request.user)
    else:
        airport.favorited_by.add(request.user)

    return redirect("airport_detail", icao=icao)


@login_required
def favorite_airports(request):

    favorites = request.user.favorite_airports.all()

    return render(request, "favorites.html", {
        "favorites": favorites
    })