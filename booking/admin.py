from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'total_price', 'booking_status', 'created_at')
    search_fields = ('user__username', 'room__room_name', 'booking_status')
    list_filter = ()
    list_editable = ('booking_status',) # Allow direct editing of status from list view
    raw_id_fields = ('user', 'room',) # Use raw_id_fields for ForeignKey to improve performance for many users/rooms

admin.site.register(Booking, BookingAdmin)