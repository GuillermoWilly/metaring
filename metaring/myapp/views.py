from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
from .utils import get_metar_from_icao


def home(request):
    metar_data = get_metar_from_icao("LEMG")  # ejemplo Sevilla
    
    context = {
        "metar": metar_data
    }
    
    return render(request, "home.html", context)

def todos(request):
    items = TodoItems.objects.all()
    return render(request, "todos.html", {"todos": items})


def airport_detail(request, icao):
    airport = get_object_or_404(Airports, icao=icao.upper())
    metar_data = get_metar_from_icao(icao.upper())

    return render(request, "airport_detail.html", {
        "airport": airport,
        "metar": metar_data
    })
