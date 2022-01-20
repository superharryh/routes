from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from .forms import RouteForm, RouteModelForm
from trains.models import Train
from cities.models import City

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

# сохраняем введенные пользователем данные конкретного маршрута
def add_route(request):
    if request.method == "POST": # для последующего сохранения маршрута, должен быть request post, т.е. нажать кнопку сохранить
        context = {} # сюда запишутся все данные (информация) того маршрута, который мы хотим сохранить в БД
        data = request.POST # в data сохраняем ВСЕ данные необходимого (для сохранения в БД) маршрута
        if data:
            #получаем данные из формы в route_form.html (те данные маршрутов, которые хочет пользователь сохранить)
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            print(trains)
            trains_lst = [int(t) for t in trains if t.isdigit()]
            print(trains_lst)
            # получаем поезда по id (собранному из данных выше)
            trains_qs = Train.objects.filter(id__in=trains_lst).select_related('from_city', 'to_city')
            # получаем города по id и переводим его в словарь с помощью in_bulk():
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk() # здесь мы за 1 запрос получили 2 необходимых значения
            print(trains_qs)
            
            # загружаем все вытащенные данные из HTML страницы в форму:
            form = RouteModelForm(
                initial= { # с помощью initial загружаем все вытащенные данные из HTML страницы в форму RouteModelForm из routes/forms.py:
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'travel_times': total_time,
                    'trains': trains_qs,
                } # ключи - это поля в форме RouteModelForm : значения - данные вытащенные из HTML файла (с помощью загруженных в <form></form> данных по каждому маршруту)
            )

            context['form'] = form


        return render(request, 'routes/create.html', context)

    else: # еслт пользователь не заполняя форму, просто через адресную строку напишет url адрес для функции add_route, то выдаст ошибку
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect ('/')

# сохранение формы в БД:
def save_route(request):
    if request.method == "POST": 
        form = RouteModelForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Маршрут успешно сохранен!')
            return redirect ('/')

        return render(request, 'routes/create.html', {'form': form})

    else: 
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect ('/')

    
