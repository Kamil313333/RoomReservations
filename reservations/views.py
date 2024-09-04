from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Reservation
from .forms import CustomUserCreationForm, ReservationForm, RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime



@login_required
def home(request):
    form = ReservationForm(request.GET or None)
    available_rooms = None

    if form.is_valid():
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']
        
        # Wyklucz pokoje, które są zarezerwowane w wybranym okresie
        reserved_rooms = Reservation.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)
        
        available_rooms = Room.objects.exclude(id__in=reserved_rooms)

    return render(request, 'home.html', {
        'form': form,
        'available_rooms': available_rooms,
    })

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
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if request.method == 'POST':
        # Konwersja daty na obiekt datetime
        check_in = datetime.strptime(check_in, '%Y-%m-%d')
        check_out = datetime.strptime(check_out, '%Y-%m-%d')
        # Przekształcenie na timezone-aware datetime
        check_in = timezone.make_aware(check_in, timezone.get_default_timezone())
        check_out = timezone.make_aware(check_out, timezone.get_default_timezone())

        reservation = Reservation.objects.create(
            room=room,
            user=request.user,
            check_in=check_in,
            check_out=check_out,
            status='active'
        )
        return redirect('reservation_list')  # Przekierowanie do strony potwierdzenia

    return render(request, 'book_room.html', {
        'room': room,
        'check_in': check_in,
        'check_out': check_out
    })

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

def available_rooms(request):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if check_in and check_out:
        try:
            # Konwersja daty na obiekt datetime
            check_in = datetime.strptime(check_in, '%Y-%m-%d')
            check_out = datetime.strptime(check_out, '%Y-%m-%d')
            # Przekształcenie na timezone-aware
            check_in = timezone.make_aware(check_in, timezone.get_default_timezone())
            check_out = timezone.make_aware(check_out, timezone.get_default_timezone())

            # Filtracja pokoi, które są dostępne w zadanym okresie
            available_rooms = Room.objects.filter(
                is_available=True
            ).exclude(
                Q(reservation__check_in__lt=check_out, reservation__check_out__gt=check_in, reservation__status='active')
            )
        except ValueError:
            available_rooms = Room.objects.none()  # Jeśli daty są niepoprawne
    else:
        available_rooms = Room.objects.all()

    return render(request, 'available_rooms.html', {
        'rooms': available_rooms,
        'check_in': check_in,
        'check_out': check_out
    })

def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    return render(request, 'room_detail.html', {
        'room': room,
        'check_in': check_in,
        'check_out': check_out
    })

def add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('room_list')  # Przekierowanie na listę pokoi po dodaniu
    else:
        form = RoomForm()
    return render(request, 'reservations/add_room.html', {'form': form})

def edit_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_detail', room_id=room.id)  # Przekierowanie na stronę szczegółów po edycji
    else:
        form = RoomForm(instance=room)
    return render(request, 'reservations/edit_room.html', {'form': form, 'room': room})