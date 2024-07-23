# reservations/urls.py

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
]