from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import *
from .utils import get_metar_from_icao, get_metar_decoded


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
    force_refresh = request.GET.get("refresh")
    metar_data = get_metar_from_icao(icao.upper(), force_refresh=bool(force_refresh))
    return render(request, "airport_detail.html", {
        "airport": airport,
        "metar": metar_data
    })

def airport_decoded(request, icao):

    airport = get_object_or_404(Airports, icao=icao.upper())
    force_refresh = request.GET.get("refresh")
    metar = get_metar_decoded(icao.upper(), force_refresh=bool(force_refresh))
    context = {
        "airport": airport,
        "metar": metar
    }

    return render(request, "airport_decoded.html", context)

def airport_compare(request):

    icao1 = request.GET.get("icao1")
    icao2 = request.GET.get("icao2")
    force_refresh = request.GET.get("refresh")
    
    error = None
    metar1 = None
    metar2 = None

    if icao1 and icao2 and icao1.upper() == icao2.upper():
        error = "Departure and destination ICAO codes cannot be the same."
    else:
        if icao1:
            metar1 = get_metar_decoded(icao1.upper(), force_refresh=bool(force_refresh))
        if icao2:
            metar2 = get_metar_decoded(icao2.upper(), force_refresh=bool(force_refresh))

    context = {
        "icao1": icao1,
        "icao2": icao2,
        "metar1": metar1,
        "metar2": metar2,
        "error": error,
    }

    return render(request, "airport_compare.html", context)


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