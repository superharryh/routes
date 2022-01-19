from django.db import models

# Create your models here.
from cities.models import City
class Route(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название маршрута')
    travel_times = models.PositiveSmallIntegerField(verbose_name='Общее время в пути')
    from_city = models.ForeignKey(to=City, on_delete=models.CASCADE, 
                                    related_name='route_from_city_set', 
                                    verbose_name='Из какого города')
    to_city = models.ForeignKey(to='cities.City', on_delete=models.CASCADE, # = to=City
                                    related_name='route_to_city_set', 
                                    verbose_name='В какой города')
    trains = models.ManyToManyField('trains.Train', verbose_name='Список поездов')
    
    def __str__(self):
        return f"Маршрут {self.name} из города {self.from_city} в город {self.to_city}"

    #изменить название самой модели и ее объектов в админ:
    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        #задаем порядок объектов модели по алфавиту:
        ordering = ['travel_times']
