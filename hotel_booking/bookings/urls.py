from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('payment/<str:room_id>/', views.payment, name='payment'),
    path('booking_history/', views.booking_history, name='booking_history'),
    path('confirm/', views.confirm_booking, name='confirm_booking'),
]