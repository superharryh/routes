from django.db import models
from django.urls import reverse

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Город') 

    #функция отображения объектов в админ панеле:
    def __str__(self):
        return self.name

    #изменить название самой модели и ее объектов в админ:
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        #задаем порядок объектов модели по алфавиту:
        ordering = ['name']
    
    # def get_absolute_url(self): # or можно использовать success_url в views.py в той view, в которой создаем объект
    # # позволяет Django переходить на страницу city_detail.html этого только что созданного объекта.
    #     return reverse('app_cities:detail', kwargs={'pk':self.pk})