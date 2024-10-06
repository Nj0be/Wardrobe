from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordMixin, AuthenticationForm
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
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1, password2 = CustomSetPasswordMixin.create_password_fields()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class UserAuthenticatorForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))
    error_messages = {
        "invalid_login": _("Your %(username)s and password didn't match. Please try again."),
        "inactive": _("This account is inactive."),
    }


class UserUpdateForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1, password2 = CustomSetPasswordMixin.create_password_fields()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
