"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from routes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('find_routes/', views.find_routes, name='find_routes'),
    path('add_route/', views.add_route, name='add_route'),
    path('save_route/', views.save_route, name='save_route'),
    path('routes_list/', views.RouteListView.as_view(), name='routes_list'),
    path('route_detail/<int:pk>', views.RouteDetailView.as_view(), name='route_detail'),
    path('route_delete/<int:pk>', views.RouteDeleteView.as_view(), name='route_delete'),

    path('cities/', include(('cities.urls', 'app_cities'))),
    path('trains/', include(('trains.urls', 'app_trains'))),
    path('accounts/', include(('accounts.urls', 'accounts'))),

    
]
