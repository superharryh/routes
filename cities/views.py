from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from .models import City
from .forms import CityForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# def cities_list(request):
#     #put CityForm from forms.py:
#     # if request.method == 'POST':
#     #     form = CityForm(request.POST)
#     #     if form.is_valid(): #if from is valid
#     #         print(form.cleaned_data) #this will print form - {'name': 'Москва'} in terminal
#     #         form.save() # we can save this form to DB
#     form = CityForm()

#     #make cities' queryset to list all cities on the page
#     cities_qs = City.objects.all()

#     # делаем пагинацию списка городов на основе функции (необязательно, лучше на основе ListView):
#     cities_list = Paginator(object_list=cities_qs, per_page=3)
#     page_number = request.GET.get('page')
#     page_obj = cities_list.get_page(page_number)

#     context = {'page_obj': page_obj, 'form' : form}
#     return render (request, 'cities/cities_homepage.html', context)


class CityDetailView(DetailView):
    context_object_name = "city_detail"
    queryset = City.objects.all()
    

class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/city_create.html'
    success_url = reverse_lazy('app_cities:list_of_cities')
    # указывается для того, чтобы Django знал,
    # куда нас перенаправлять после успешного создания нового города в форме 
    # (которая наследуется от модели). Обязательно тут использовать reverse_lazy!
    success_message = "Город успешно добавлен!"

class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/city_update.html'
    success_url = reverse_lazy('app_cities:list_of_cities')
    success_message = "Город успешно отредактирован!"

class CityDeleteView(SuccessMessageMixin, DeleteView):
    model = City
    template_name = 'cities/city_delete.html'
    success_url = reverse_lazy('app_cities:list_of_cities')
    success_message = "Город успешно удалён!"



class CityListView(ListView):
    model = City
    paginate_by = 3
    template_name = 'cities/cities_homepage.html'