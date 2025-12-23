from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'image', 'room_number', 'room_type', 'price_per_night', 'max_guests')
    search_fields = ('room_name', 'room_number', 'description')
    list_filter = ()
    exclude = ('amenities',)

admin.site.register(Room, RoomAdmin)