import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))
        
        if not re.search(r'\d', password):
            raise ValidationError(_('Password must contain at least one digit.'))
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_('Password must contain at least one special character.'))

    def get_help_text(self):
        return _('Password must be at least 8 characters long, contain at least one digit and one special character.')

def validate_username(username):
    """
    Walidator nazwy użytkownika: wymaga minimalnej długości i sprawdza, czy nazwa użytkownika
    składa się tylko z liter, cyfr i podkreśleń.
    """
    if len(username) < 4:
        raise ValidationError(_('Username must be at least 4 characters long.'))
    
    if not re.match(r'^\w+$', username):
        raise ValidationError(_('Username can only contain letters, digits, and underscores.'))

def validate_email(email):
    """
    Walidator e-maila: sprawdza poprawność formatu adresu e-mail.
    """
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email):
        raise ValidationError(_('Enter a valid email address.'))