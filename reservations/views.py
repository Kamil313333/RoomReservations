from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Reservation
from .forms import CustomUserCreationForm, ReservationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

@login_required
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation_list.html', {'reservations': reservations})

@login_required
def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Zapisz użytkownika w bazie danych
            login(request, user) # Automatyczne logowanie użytkownika po rejestracji
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room = room
            reservation.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'book_room.html', {'room': room, 'form': form})

@login_required
def reservation_list(request):
    # Aktualizacja statusu rezerwacji przed wyświetleniem listy
    current_time = timezone.now()
    expired_reservations = Reservation.objects.filter(check_out__lt=current_time, status='active')
    expired_reservations.update(status='expired')
    
    # Pobranie zaktualizowanych rezerwacji użytkownika
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation_list.html', {'reservations': reservations})

def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Możesz wysłać e-mail lub zapisać dane do bazy
            send_mail(
                f"Contact Form Submission from {name}",
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Przekierowuje na stronę kontaktową po udanym wysłaniu
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})