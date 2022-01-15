from trains import views
from django.urls import path

urlpatterns = [
    path('', views.TrainListView.as_view(), name='list_of_trains'), 
    path('detail/<int:pk>', views.TrainDetailView.as_view(), name='detail'), 
    path('add/', views.TrainCreateView.as_view(), name='create'), 
    path('update/<int:pk>', views.TrainUpdateView.as_view(), name='update'), 
    path('delete/<int:pk>', views.TrainDeleteView.as_view(), name='delete'), 
]
