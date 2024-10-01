from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordMixin
from django.utils.translation import gettext as _
from django.contrib.auth import password_validation
from .models import User


class CustomSetPasswordMixin(SetPasswordMixin):
    @staticmethod
    def create_password_fields(label1=_("Password"), label2=_("Password confirmation")):
        password1 = forms.CharField(
            label=label1,
            required=True,
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            help_text=password_validation.password_validators_help_text_html(),
        )
        password2 = forms.CharField(
            label=label2,
            required=True,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            strip=False,
            help_text=_("Enter the same password as before, for verification."),
        )
        return password1, password2


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1, password2 = CustomSetPasswordMixin.create_password_fields()

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
