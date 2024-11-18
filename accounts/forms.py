from django import forms
from django.contrib.auth.forms import SetPasswordMixin, AuthenticationForm, BaseUserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth import password_validation
from .models import User


class UserRegisterForm(BaseUserCreationForm):
    first_name = forms.CharField(
        label = "Nome",
        widget=forms.TextInput(),
        required = True,
    )

    last_name = forms.CharField(
        label = "Cognome",
        widget=forms.TextInput(),
        required=True,
    )

    email = forms.EmailField(
        label = "Email",
        error_messages={"invalid": "Perfavore inserisci una email valida"},
        required=True,
    )

    password1 = forms.CharField(
        label = "Password",
        required=True,
        widget=forms.PasswordInput(),
    )

    password2 = forms.CharField(
        label="Conferma Password",
        required=True,
        widget=forms.PasswordInput(),
    )

    error_messages = {
        "password_mismatch": _("Le due password non corrispondono."),
    }

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class UserAuthenticatorForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))
    username.widget.attrs = {
        'id': 'email',
        'name': 'email',
        'type': 'email',
        'required': True,
        'autocomplete': "email",
        'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6'
        }
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    password.widget.attrs = {
        'id': 'password',
        'name': 'password',
        'type': 'password',
        'required': True,
        'autocomplete': "current-password",
        'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6'
    }

    error_messages = {
        "invalid_login": _("La tua email e password non corrispondono. Perfavore prova di nuovo."),
        "inactive": _("Il tuo account è inattivo."),
    }


class UserUpdateForm(BaseUserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1, password2 = SetPasswordMixin.create_password_fields()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
