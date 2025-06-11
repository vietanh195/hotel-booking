from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.home, name='home'),
    path('room_list/', views.room_list, name='room_list'),
    path('room_detail/<str:room_id>/', views.room_detail, name='room_detail'),
]