from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Город') 

    #функция отображения объектов в админ панеле:
    def __str__(self):
        return self.name

    #изменить название самой модели и ее объектов в админ:
    class Meta:
        verbose_name_plural = 'Города'
        #задаем порядок объектов модели по алфавиту:
        ordering = ['name']
    