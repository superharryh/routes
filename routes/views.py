from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from .forms import RouteForm

from .get_routes_func import get_routes


def home(request):
    form = RouteForm()
    return render(request, 'routes/route_form.html', {'form':form})

def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST)

        if form.is_valid(): #если заполняемая пользователем форма для поиска маршрутов валидна:
            try:
                context = get_routes(request, form) # данная функция осуществляет поиск необходимого для пользователя маршрута
            except ValueError as e: # если в ведённых пользователем полях и полях готового маршрута есть хотя бы одно несоответствие, то
                messages.error(request, e) #вывадим ошибку в виде этого несоответствия, чтобы пользователь смог это несоответствие исправить
                return render(request, 'routes/route_form.html', {'form':form})
            return render(request, 'routes/route_form.html', context)

        #если заполняемая пользователем форма для поиска маршрутов не валидна:
        return render(request, 'routes/route_form.html', {'form':form})

    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')
        return render(request, 'routes/route_form.html', {'form':form})

    
