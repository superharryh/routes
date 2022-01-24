from django.test import TestCase

# Create your tests here.
from cities.models import City
from trains.models import Train
from django.core.exceptions import ValidationError
from django.urls import reverse

from routes import views as routes_view
from cities import views as cities_view
from routes.forms import RouteForm

from routes.get_routes_func import get_graph, dfs_paths, get_routes

class AllTestCase(TestCase):
    def setUp(self): # здесь мы будем прописывать начальные данные, которые позже будем тестировать:
        # получаем экземпляры городов и записываем их в тестирование-БД 
        # (так как они нам понадобятся впоследствии при создании поездов и маршрутов)
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        # создаем поезда между этими городами и записываем их в тестирование-БД:
        trains_lst = [
            Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9),
            Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=8),
            Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=7),
            Train(name='t4', from_city=self.city_C, to_city=self.city_B, travel_time=6),
            Train(name='t5', from_city=self.city_B, to_city=self.city_E, travel_time=3),
            Train(name='t6', from_city=self.city_B, to_city=self.city_A, travel_time=11),
            Train(name='t7', from_city=self.city_A, to_city=self.city_C, travel_time=10),
            Train(name='t8', from_city=self.city_E, to_city=self.city_D, travel_time=5),
            Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=4),
        ]
        Train.objects.bulk_create(trains_lst) # создаст набор поездов в БД
        # bulk_create method inserts the provided list of objects into the database 
        # in an efficient manner (generally only 1 query, no matter how many objects there are), 
        # and returns created objects as a list, in the same order as provided:
        # objs = Entry.objects.bulk_create([
        # Entry(headline='This is a test'),
        # Entry(headline='This is only a test'),
        # ])

    #! 1.) проверка невозможности создания дублей (одинаковых) городов, т.е. дублей тех городов, которые уже есть в БД:
    def test_model_city_duplicate(self):
        """Тестирование возникновения ошибки при создании дубля города"""
        # 1) создаем проверочный экземпляр класса City, но он не будет записан в БД:
        city = City(name="A")

        # 2.1) в этих тестах заведомо прописываем исключения и ошибки, на которые должно сработать assertRaises;
        # 2.2) ValidationError это то изменение, которое мы планируем поймать в ходе тестирования, 
        # т.е. оно должно быть вызвано в ходе тестирования в терминале => test - OK
        with self.assertRaises(ValidationError): 

            # 3) здесь - пишем тот код, который должен вызвать это исключение:
            city.full_clean() # проверяем является ли city экземпляр таким, который проходит все проверки (но мы ожидаем ошибку)
            # у нас есть важный параметр - name - и он должен быть уникальным => 
            # у экземпляра модели City, есть метод full_clean(), 
            # который проводит полную проверку соответствия того, 
            # что мы ранее прописали в модели (def setUp(self):) по тому, 
            # какие данные сейчас имеются в экземпляре city;
            #* чтобы тестирование прошло OK, нужно поймать ошибку assertRaises(ValidationError),
            #* которая будет означать, что экземпляр city с name='A' уже есть в БД, и снова его нельзя записать в БД
    
    def test_model_train_duplicate(self):
        '''Тестирование возникновения ошибки при создании дубля поезда'''
        # проверяем уникальность name в классе Train:
        train = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=129)

        with self.assertRaises(ValidationError): 
            # так как поездов с одинаковми названиями не может быть, 
            # поэтому ловим ValidationError => тестирование OK
            train.full_clean()

    def test_model_trainsdata_duplicate(self):
        # проверяем уникальность данных самого поезда, независимо от name, так как данные поездов должны отличаться:
        train = Train(name='t121212212', from_city=self.city_A, to_city=self.city_B, travel_time=9)

        with self.assertRaises(ValidationError): 
            # так как поездов с одинаковыми города отправления и прибытия, а также одинаковым временем не может быть в БД, 
            # поэтому ловим ValidationError => тестирование OK
            train.full_clean()

        # проверяем, чтобы сообщение, выпадающее при заполнении поезда 
        # было действительно - ('Такой поезд уже существует! Измените время в пути или города.') :
        try:
            train.full_clean()
        except ValidationError as e:
            self.assertEqual({'__all__': ['Такой поезд уже существует! Измените время в пути или города.']}, e.message_dict)
            # эти данные получили при помощи debugging в тестировании чему равно e
            # OR
            self.assertIn('Такой поезд уже существует! Измените время в пути или города.', e.messages)
    
    #! 2.) проверка валидации шаблонов и функций:
    def test_home_routes_views(self):
        # получаем ответ от сервера (по url из urls.py) - делаем запрос браузера к серверу:
        # проверяем корректность работы начальной страницы - home (где поиск маршрута):
        response = self.client.get(reverse('home')) # получаем состояние работы начальной страницы - home
        # client - отвечает за регулирование работы браузера

        # 1) от HTML страницы проверяем удачный ответ (response), который равен 200:
        self.assertEqual(200, response.status_code) 
        # 2) проверяем правльность используемого шаблона на url - home:
        self.assertTemplateUsed(response, template_name='routes/route_form.html') # template_name указан в views.py в фцнкции home
        # 3) проверяем правильность использованной функции для адреса url - home:
        self.assertEqual(first=response.resolver_match.func, second=routes_view.home)
    
    def test_city_cbv_detail_views(self):
        response = self.client.get(reverse('app_cities:detail', kwargs={'pk': self.city_A.id})) 
        # как в шаблоне city_homepage.html с сылкой на каждый city

        # 1) от HTML страницы проверяем удачный ответ (response), который равен 200:
        self.assertEqual(200, response.status_code) 
        # 2) проверяем правльность используемого шаблона на url - app_cities:detail/<int:pk> - name='detail' :
        self.assertTemplateUsed(response, template_name='cities/city_detail.html') # template_name указан в views.py в фцнкции home
        # 3) проверяем правильность использованной функции для адреса url - app_cities:detail/<int:pk> - name='detail' :
        self.assertEqual(first=response.resolver_match.func.__name__, 
                         second=cities_view.CityDetailView.as_view().__name__) #* так делать для проверки CBV

    #! 3.) Тестирование работоспособности функций построения графа и поиска маршрута:
    def test_find_all_routes(self):
        # 1) создаем кверисет из поездов:
        qs = Train.objects.all()
        # 2) этот кверисет превращаем в граф:
        graph = get_graph(qs)
        # 3) получаем все маршруты:
        all_routes = list(dfs_paths(graph, self.city_A.id, self.city_E.id)) # из города А в город Е есть 4 маршрута =>:
        self.assertEqual(len(all_routes), 4)
    
    #! 4.) Тестирование валидности формы поиска маршрута:
    def test_valid_route_form(self):
        data = {"from_city": self.city_A.id, 
                "to_city": self.city_B.id,
                "cities": [self.city_E.id, self.city_D.id],
                "all_travel_time": 9,
        }
        # создаем экземпляр формы на основе нашей data:
        form = RouteForm(data=data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_route_form(self):
        # проверяет валидность формы: 
        data = {'from_city': self.city_A.id, 'to_city': self.city_B.id,
                'cities': [self.city_E.id, self.city_D.id],
                } # не указали поле all_travel_time => должно сработать условие self.assertFalse(form.is_valid())
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())
        
        # поле all_travel_time - это IntegerField() => "all_travel_time": 9.99 - ошибка - форма невалидна
        data = {"from_city": self.city_A.id, 
                "to_city": self.city_B.id,
                "cities": [self.city_E.id, self.city_D.id],
                "all_travel_time": 9.99,
        }
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())

    #! 5.) Тестирование сообщений об ошибках:
    def test_message_error_time_less(self):
        # 1) задаем реальный маршрут:
        data = {"from_city": self.city_A.id, 
                "to_city": self.city_E.id,
                "cities": [self.city_C.id],
                "all_travel_time": 9
        }
        # 2) делаем response, т.е. через запрос будем обращаться к сообщениям:
        response = self.client.post('/find_routes/', data) # через метод post отправляем на адрес url - find_routes, который принимает данные
        # 3) получаем ответ и проверяет есть ли в этом ответе нужное для нас сообщение 
        # (которое мы ожидаем получить после заполнения формы поиска маршрута):
        self.assertContains(response, 'Указанное время в пути меньше доступного для данного маршрута.', 1, 200)

    def test_message_error_cross_cities(self):
        # 1) задаем реальный маршрут:
        data = {"from_city": self.city_B.id, 
                "to_city": self.city_E.id,
                "cities": [self.city_C.id],
                "all_travel_time": 11119
        }
        # 2) делаем response, т.е. через запрос будем обращаться к сообщениям:
        response = self.client.post('/find_routes/', data) # через метод post отправляем на адрес url - find_routes, который принимает данные
        # 3) получаем ответ и проверяет есть ли в этом ответе нужное для нас сообщение 
        # (которое мы ожидаем получить после заполнения формы поиска маршрута):
        self.assertContains(response, 'Машрут через эти города невозможен.', 1, 200)




    
        






