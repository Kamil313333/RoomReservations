# reservations/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Dodano przekierowanie na login po wylogowaniu
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('contact/', views.contact, name='contact'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('contact/', views.contact_form, name='contact_form'),
    path('available_rooms/', views.available_rooms, name='available_rooms'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room/add/', views.add_room, name='add_room'),
    path('room/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', views.logout_view, name='logout_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)