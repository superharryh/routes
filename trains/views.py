from trains.models import Train
from .forms import TrainForm

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin



class TrainListView(ListView):
    model = Train
    paginate_by = 3
    template_name = 'trains/trains_homepage.html'

class TrainDetailView(DetailView):
    context_object_name = "train_detail" 
    queryset = Train.objects.all()
    template_name = 'trains/train_detail.html'


class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/train_create.html'
    success_url = reverse_lazy('app_trains:list_of_trains')
    # указывается для того, чтобы Django знал,
    # куда нас перенаправлять после успешного создания нового города в форме 
    # (которая наследуется от модели). Обязательно тут использовать reverse_lazy!
    success_message = "Поезд успешно добавлен!"

class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/train_update.html'
    success_url = reverse_lazy('app_trains:list_of_trains')
    success_message = "Поезд успешно отредактирован!"

class TrainDeleteView(SuccessMessageMixin, DeleteView):
    model = Train
    template_name = 'trains/train_delete.html'
    success_url = reverse_lazy('app_trains:list_of_trains')
    success_message = "Поезд успешно удалён!"