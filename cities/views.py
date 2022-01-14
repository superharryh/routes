from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import City
from .forms import CityForm
from django.urls import reverse_lazy

def cities_list(request):
    #put CityForm from forms.py:
    # if request.method == 'POST':
    #     form = CityForm(request.POST)
    #     if form.is_valid(): #if from is valid
    #         print(form.cleaned_data) #this will print form - {'name': 'Москва'} in terminal
    #         form.save() # we can save this form to DB
    form = CityForm()
    #make cities' queryset to list all cities on the page
    cities_qs = City.objects.all()
    context = {'cities_list': cities_qs, 'form' : form}
    return render (request, 'cities/cities_homepage.html', context)


class CityDetailView(DetailView):
    context_object_name = "city_detail"
    queryset = City.objects.all()
    

class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/city_create.html'
    success_url = reverse_lazy('app_cities:cities')
    # указывается для того, чтобы Django знал,
    # куда нас перенаправлять после успешного создания нового города в форме 
    # (которая наследуется от модели). Обязательно тут использовать reverse_lazy!

class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/city_update.html'
    success_url = reverse_lazy('app_cities:cities')

class CityDeleteView(DeleteView):
    model = City
    template_name = 'cities/city_delete.html'
    success_url = reverse_lazy('app_cities:cities')
