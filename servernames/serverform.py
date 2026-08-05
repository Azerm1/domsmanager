from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import servername

class serverform(ModelForm):
    class Meta:
        model = servername
        fields = ["name", "startdate", "enddate"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class":"input",
                "placeholder":"example.com"
            }),
            "startdate": forms.DateInput(attrs={
                "class":"input",
                "type":"date"
            }),
            "enddate": forms.DateInput(attrs={
                "class":"input",
                "type":"date"
            }),}
    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("startdate")
        end = cleaned.get("enddate")
        if start and end and end < start:
            raise ValidationError("End date must be after start date.")
        return cleaned