from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import CustomPasswordValidator, validate_username, validate_email

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