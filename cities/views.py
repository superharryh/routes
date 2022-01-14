from .models import City
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

def cities_list(request):
    cities_qs = City.objects.all()
    context = {'cities_list': cities_qs}
    return render (request, 'cities/cities_homepage.html', context)


class CityDetailView(DetailView):
    context_object_name = "city_detail"
    queryset = City.objects.all()
    template_name = 'cities/city_detail.html'