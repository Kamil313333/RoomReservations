from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import CustomPasswordValidator, validate_username, validate_email
from .models import Reservation, Room

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    username = forms.CharField(validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'minlength': '8'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].help_text = 'Password must be at least 8 characters long, contain at least one digit and one special character.'
        self.fields['username'].help_text = 'Username must be at least 4 characters long and only contain letters, digits, and underscores.'
        self.fields['email'].help_text = 'Enter a valid email address.'

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        CustomPasswordValidator().validate(password)  # Używamy klasy walidatora
        return password
    
class ReservationForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Check-in Date"
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Check-out Date"
    )

    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out']   

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'capacity', 'is_available', 'description', 'price_per_night', 'image', 'amenities', 'size', 'bed_type', 'view']