from cities import views
from django.urls import path

urlpatterns = [
    path('', views.cities_list, name='cities'), 
    path('detail/<int:pk>', views.CityDetailView.as_view(), name='detail'), 
]
