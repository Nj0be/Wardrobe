from django import forms
from django.core.validators import RegexValidator
from django.forms.models import ModelForm
from django.utils.text import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["title", "description", "vote"]
        VOTE_CHOICES = ((1, "★"), (2, "★"*2), (3, "★"*3), (4, "★"*4), (5, "★"*5))
        labels = {
            "title": "Titolo",
            "description": "Descrizione",
            "vote": "Voto",
        }
        widgets = {
            'title': forms.TextInput(attrs={'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'placeholder': 'Scrivi qui la tua recensione', 'rows': '4', 'autocomplete': 'off'}),
            'vote': forms.RadioSelect(choices=VOTE_CHOICES, attrs={'class': 'hidden peer', 'autocomplete': 'off'}),
        }
