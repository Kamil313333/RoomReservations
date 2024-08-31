# reservations/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_view, name='logout'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('reservations/', views.reservation_list, name='reservation_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

