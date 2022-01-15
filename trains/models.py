from django.db import models

# Create your models here.
from cities.models import City

from django.core.exceptions import ValidationError
class Train(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Номер поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(to=City, on_delete=models.CASCADE, 
                                    related_name='from_city_set', 
                                    verbose_name='Из какого города')
    to_city = models.ForeignKey(to='cities.City', on_delete=models.CASCADE, # = to=City
                                    related_name='to_city_set', 
                                    verbose_name='В какой города')
    #можно так указать модель, на которую ссылается этот ключ 'cities.City',
    # это можно использовать в том случае, чтобы избежать перекрёстного испорта моделей.

    def __str__(self):
        return f"Поезд № {self.name} из города {self.from_city} в город {self.to_city}"

    #изменить название самой модели и ее объектов в админ:
    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        #задаем порядок объектов модели по алфавиту:
        ordering = ['travel_time']

    # Проверка форм и полей формы:
    # прописываем проверку валидации полей перед сохранением данных в БД:
    def clean(self):
        #1) проверяем, чтобы при заполнении полей таблицы не было кольцевания поезда, 
        # т.е. города прибытия и отправки должны быть разными:  
        if self.from_city == self.to_city:
            raise ValidationError ('Измените город прибытия или отправки.')

        #2) исключить создание повторных поездов,
        # т.е. создаем queryset с помощью запроса в БД,  
        # и затем с помощью if проверяем есть ли создаваемый поезд уже в БД,
        # если есть - то выдаем ошибку, что нужно создать другой поезд, так как этот уже записан в БД:
        train_qs = Train.objects.filter(from_city=self.from_city,  # Train == self__class__
                                        to_city=self.to_city, 
                                        travel_time=self.travel_time).exclude(pk=self.pk)
        # exclude(pk=self.pk) исключает создание ошибки при редактировании уже существующего поезда.
        if train_qs.exists(): #Если данный поезд уже существует в БД:
            raise ValidationError ('Такой поезд уже существует! Измените время в пути или города.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

