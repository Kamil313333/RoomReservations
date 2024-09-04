from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.urls import reverse

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='rooms/', blank=True)

    # Dodajemy brakujące pola
    bed_type = models.CharField(max_length=50, blank=True, choices=[('Single', 'Single'), ('Double', 'Double'), ('Queen', 'Queen'), ('King', 'King')])
    size = models.IntegerField(help_text="Size of the room in square meters", blank=True, null=True)
    view = models.CharField(max_length=100, blank=True, choices=[('Sea', 'Sea'), ('Mountain', 'Mountain'), ('City', 'City')])
    amenities = models.TextField(help_text="List of amenities separated by commas", blank=True)

    def __str__(self):
        return f"Room {self.room_number}"

    def get_absolute_url(self):
        return reverse('room_detail', args=[str(self.id)])

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # Nowe pole statusu

    def save(self, *args, **kwargs):
        # Upewnij się, że check_out jest datetime i porównaj je
        if isinstance(self.check_out, str):
            self.check_out = timezone.make_aware(datetime.strptime(self.check_out, '%Y-%m-%d'), timezone.get_default_timezone())

        if self.check_out < timezone.now() and self.status == 'active':
            self.status = 'expired'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation for {self.room} by {self.user}"