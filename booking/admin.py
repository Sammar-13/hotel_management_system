from django.contrib import admin
from .models import Booking
class BookingAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = (
        'id', 
        'user', 
        'room', 
        'check_in_date', 
        'check_out_date', 
        'total_price', 
        'booking_status', 
        'is_cancelled',
        'user_dismissed',
    )
    search_fields = ('user__username', 'room__room_name', 'booking_status')
    list_editable = ('booking_status',)
    raw_id_fields = ('user', 'room',)
    ordering = ('-created_at',)
    readonly_fields = ('is_cancelled', 'cancelled_at', 'user_dismissed', 'created_at')
    actions = ['delete_selected']
admin.site.register(Booking, BookingAdmin)
