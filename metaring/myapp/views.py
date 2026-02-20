from django.shortcuts import render, HttpResponse
from .models import *
from .utils import get_metar_from_icao


def home(request):
    metar_data = get_metar_from_icao("LEZL")  # ejemplo Sevilla
    
    context = {
        "metar": metar_data
    }
    
    return render(request, "home.html", context)

def todos(request):
    items = TodoItems.objects.all()
    return render(request, "todos.html", {"todos": items})









'''class SearchView(ListView):
    model = Airport
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('search')
       if query:
          postresult = Airport.objects.filter(title__contains=query)
          result = postresult
       else:
           result = None
       return result'''