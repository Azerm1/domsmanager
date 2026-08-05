from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import User

class userform(ModelForm):
    class Meta:
        model=User
        fields=['username','email','password','first_name','last_name']
    def clean(self):
        validatedata = super().clean()
        username = validatedata.get("username")
        email = validatedata.get("email")
        password = validatedata.get("password")
        if not username:
            raise ValidationError("username is required.")
        if not email:
            raise ValidationError("email is required.")
        if not password:
            raise ValidationError("password is required.")
        if len(password) < 8:
            raise ValidationError("password must contain at least 8 characters.")
        return validatedata