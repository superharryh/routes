from django.contrib import admin

# Register your models here.
from .models import Train
class TrainAdmin(admin.ModelAdmin):
    class Meta:
        model = Train
    list_display = ('name', 'from_city', 'to_city', 'travel_time')
    list_editable = ('travel_time',) # тут лучше не писать много, так как идет большая нагрузка ан сервер

admin.site.register(Train, TrainAdmin)