from django.urls import path
from cities.views import *

urlpatterns = [
    path('city_list', cities, name=cities), #name=home 
]