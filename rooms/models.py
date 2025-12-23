from django.db import models
from django.utils import timezone

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True) # e.g., 'wifi', 'tv', 'ac'

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    )
    room_number = models.CharField(max_length=10, unique=True)
    room_name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='Single')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    max_guests = models.IntegerField(default=1)
    amenities = models.ManyToManyField(Amenity, blank=True)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True) # Main image for the room listing
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.room_name} ({self.room_type} - {self.room_number})"


