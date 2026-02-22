from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("accounts/register/", views.register, name="register"),
    path("airport/<str:icao>/", views.airport_detail, name="airport_detail"),
    path("airport/<str:icao>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/", views.favorite_airports, name="favorites"),
]