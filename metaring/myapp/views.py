from django.shortcuts import render, HttpResponse
from .models import TodoItems
def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItems.objects.all()
    return render(request, "todos.html", {"todos": items})