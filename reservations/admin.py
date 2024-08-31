from django.contrib import admin
from .models import Room, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'capacity', 'is_available', 'price_per_night')
    list_filter = ('is_available',)
    search_fields = ('room_number',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image.url if obj.image else "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'check_in', 'check_out', 'status', 'created_at')
    list_filter = ('status', 'check_in', 'check_out', 'room')
    search_fields = ('room__room_number', 'user__username')