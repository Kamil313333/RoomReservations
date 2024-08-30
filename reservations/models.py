from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)  # Pole na opis pokoju
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)  # Cena za noc
    image = models.ImageField(upload_to='', blank=True)  # Zdjęcie pokoju

    def __str__(self):
        return f"Room {self.room_number}"

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.room} by {self.user}"