from cities import views
from django.urls import path

urlpatterns = [
    # path('', views.cities_list, name='cities'), 
    path('', views.CityListView.as_view(), name='list_of_cities'), 
    path('detail/<int:pk>', views.CityDetailView.as_view(), name='detail'), 
    path('add/', views.CityCreateView.as_view(), name='create'), 
    path('update/<int:pk>', views.CityUpdateView.as_view(), name='update'), 
    path('delete/<int:pk>', views.CityDeleteView.as_view(), name='delete'), 
    
]
