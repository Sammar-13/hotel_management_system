from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:pk>/', views.cancel_booking, name='cancel_booking'),
]
