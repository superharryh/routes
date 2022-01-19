from trains.models import Train

def dfs_paths(graph, start, finish):
    """Функция поиска всех возможных маршрутов из одного города в другой. 
    Вариант посещения одного и того же города более одного раза не рассматривается"""
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == finish:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))

def get_graph(qs):
    graph = {}
    for i in qs:
        graph.setdefault(i.from_city_id, set())
        graph[i.from_city_id].add(i.to_city_id)
    return graph

def get_routes(request, form) -> dict:
    context = {'form': form}

    qs = Train.objects.all().select_related('from_city', 'to_city') # print(qs.query)
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    all_travel_time = data['all_travel_time']
    cities = data['cities']
    all_ways = list(dfs_paths(graph=graph, start=from_city.id, finish=to_city.id))
    
    if not len(all_ways):
        raise ValueError('Машрута, удовлетворяющего условиям не существует.')

    if cities: # если пользователь указал какие-то города, через которые нужно проехать, чтобы добраться из пункта А в пункт Б
        #1) получаем список всех id городов, через которые нужно проехать, указанные пользователем:
        _cities = [city.id for city in cities] 

        right_ways = [] # сюда будем добавлять те маршруты, в которых есть города, указанные пользователем
        #2) проверяем входят ли id тех городов, через которые нужно проехать, указанные пользователем 
        # во все маршруты (all_ways) из from_city в to_city, введённый ранее пользователем 
        # и на основании, которых ранее был сделан граф - all_ways:
        for route in all_ways:
            if all(city in route for city in _cities):
            # т.е. в этом цикле проходимся по всем id городов, указанные пользователем, через которые он хочет проехать,
            # и проверяем вхождение данного города в определённый маршрут по порядку из all_ways,
            # если все города, указанные пользователем (_cities) есть в данном маршруте, 
            # то этот маршрут можно добавлять в right_ways.
                right_ways.append(route)
        if not right_ways:
        # если ни один маршрут не был добавлен в right_ways 
        # (т.е. если в БД нет маршрута через города, указанные пользователем):
           raise ValueError('Машрут через эти города невозможен.') 
    else:
        right_ways = all_ways
    
    # проверяем маршруты по времени:
    right_routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    
    for route in right_ways: # для каждого маршрута из проверенных ранее и удовлетворяющих условиям - через нужные города:
        tmp = {}
        tmp["trains"] = [] # здесь мы указываем, что в нашем слвоаре tmp, будет ключ - trains и его значения - это список (но пока пустой), позже мы его заполним
        total_time = 0
        for i in range(len(route) - 1): # например, маршрут [2, 5, 9, 3, 7] , его длина - 5 и вычитаем 1, как позже мы будем прибавлять 1, чтобы двигаться вперед по id поездов в маршруте (в списке)
            qs = all_trains[(route[i], route[i+1])] # здесь мы получаем ключ в словаре в виде tuple попарно, например, 2 и 5, затем 5 и 9 и тд.

            q = qs[0]
            total_time += q.travel_time # указывам от Train model
            tmp["trains"].append(q) # в словаре tmp, trains - это ключ, а q - один поезд в маршруте, таким образом мы проверяем каждый поезд в каждом маршруте, и задаем вытаскиваем время этого поезда.


        tmp['total_time'] = total_time


        if total_time <= all_travel_time:
            right_routes.append(tmp) # right_routes - это список словарей, в котором каждый словарь - tmp, 
            # где мы знаем только знаечение tmp['total_time'] = total_time
        # print(right_routes)

    if not right_routes:
        raise ValueError('Указанное время в пути меньше доступного для данного маршрута.')

    # Сортировка маршрутов по времени:
    sorted_routes = []
    if right_routes == 1: # если получился только 1 маршрут:
        sorted_routes = right_routes
    else:
        times = list(set(r['total_time'] for r in right_routes)) # получили сет совокупного времени всех верных маршрутов
        times = sorted(times) # сортирует сет из маршрутов согласно времени

        # когла получили отсортированный сет по времени, нужно подтянуть все данные маршрута согласно времени:
        for time in times:
            for route in right_routes:
                if time == route['total_time']: # если время в сете отсортированных времен равно общему времени маршрута, в удовлетворяющем условиям словаре маршрутов
                    sorted_routes.append(route)
    # в форму, которую будем отображать на странице посел поиска, передаем полученные данные:
    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city.name, 'to_city': to_city.name}

    return context #так как этот context мы потом используем в views.py -> def find_routes(request):