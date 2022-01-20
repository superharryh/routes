
#* 3.) Добавляем login_view в urlpatterns:

from django.urls import path
from . import views 
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view, name='registration')
]