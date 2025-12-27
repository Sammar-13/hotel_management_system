from django.db import models
from django.conf import settings
from django.utils import timezone
from rooms.models import Room
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    user_dismissed = models.BooleanField(default=False, help_text="If True, hidden from user dashboard")
    cancelled_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Bookings"
    def __str__(self):
        return f"Booking {self.id} by {self.user.username} for {self.room.room_name}"
    def save(self, *args, **kwargs):
        if self.booking_status == 'cancelled':
            if not self.is_cancelled:
                self.is_cancelled = True
                self.cancelled_at = timezone.now()
        super().save(*args, **kwargs)
