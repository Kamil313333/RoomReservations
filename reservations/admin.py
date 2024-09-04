from django.contrib import admin
from django.utils.html import mark_safe
from .models import Room, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'capacity', 'is_available', 'price_per_night', 'image_preview')
    list_filter = ('is_available', 'capacity', 'price_per_night')  # Filtry według dostępności, pojemności i ceny
    search_fields = ('room_number', 'description')  # Wyszukiwanie według numeru pokoju i opisu
    readonly_fields = ('image_preview',)  # Pole do podglądu obrazu tylko do odczytu
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 150px; height: auto;" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'
    
    # Dodanie linku do strony szczegółów pokoju bezpośrednio z panelu admina
    def view_on_site(self, obj):
        return obj.get_absolute_url()
    
    # Dodanie opcji edycji z panelu admina
    fieldsets = (
        (None, {
            'fields': ('room_number', 'capacity', 'is_available', 'price_per_night', 'description', 'image')
        }),
    )

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'check_in', 'check_out', 'status', 'duration', 'created_at')
    list_filter = ('status', 'check_in', 'check_out', 'room', 'created_at')  # Filtry statusu, daty check-in, check-out, pokoju i daty utworzenia
    search_fields = ('room__room_number', 'user__username', 'status')  # Wyszukiwanie według numeru pokoju, nazwy użytkownika i statusu
    actions = ['mark_as_cancelled']

    def duration(self, obj):
        # Zwraca czas trwania rezerwacji w dniach
        return (obj.check_out - obj.check_in).days
    duration.short_description = 'Duration (days)'

    def mark_as_cancelled(self, request, queryset):
        # Niestandardowa akcja do masowego anulowania rezerwacji
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = 'Mark selected reservations as Cancelled'