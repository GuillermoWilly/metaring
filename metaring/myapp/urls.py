from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("todos/", views.todos, name="Todos"),
    path("airport/<str:icao>/", views.airport_detail, name="airport_detail"),
]