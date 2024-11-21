from django import forms
from django.core.validators import RegexValidator
from django.utils.text import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from .models import Review


class AddReviewForm(forms.Form):
    title = forms.CharField(
        label = "Titolo",
        max_length=200,
        widget=forms.TextInput(),
        required = True,
    )

    description = forms.CharField(
        label = "Descrizione",
        max_length=2000,
        widget=forms.Textarea(attrs={'placeholder': 'Scrivi qui la tua recension', 'rows': '4'}),
        required = True,
    )

    vote = forms.TypedChoiceField(
        label = "Voto",
        choices = ((1, "★"), (2, "★"*2), (3, "★"*3), (4, "★"*4), (5, "★"*5)),
        widget = forms.RadioSelect(attrs={'class': 'hidden peer'}),
        initial = '1',
        required = True,
    )
