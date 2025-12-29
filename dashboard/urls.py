from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    
    # Rooms
    path('rooms/', views.manage_rooms, name='manage_rooms'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:pk>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:pk>/', views.delete_room, name='delete_room'),
    
    # Bookings
    path('bookings/', views.manage_bookings, name='manage_bookings'),
    path('bookings/update/<int:pk>/', views.update_booking_status, name='update_booking_status'),
    
    # Users
    path('users/', views.manage_users, name='manage_users'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('users/toggle_active/<int:pk>/', views.toggle_user_active, name='toggle_user_active'),
    
    # Feedback
    path('feedback/', views.manage_feedback, name='manage_feedback'),
    path('feedback/delete/<int:pk>/', views.delete_feedback, name='delete_feedback'),
    
    # Sliders
    path('sliders/', views.manage_sliders, name='manage_sliders'),
    path('sliders/add/', views.add_slider, name='add_slider'),
    path('sliders/delete/<int:pk>/', views.delete_slider, name='delete_slider'),
    
    # Inquiries
    path('inquiries/', views.manage_inquiries, name='manage_inquiries'),
    path('inquiries/reply/<int:pk>/', views.reply_inquiry, name='reply_inquiry'),
]
