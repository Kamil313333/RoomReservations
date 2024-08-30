from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'capacity', 'is_available', 'price_per_night')
    list_filter = ('is_available',)
    search_fields = ('room_number',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image.url if obj.image else "No Image"
    image_preview.short_description = 'Image Preview'