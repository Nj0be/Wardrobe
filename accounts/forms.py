from django import forms
from django.contrib.auth.forms import SetPasswordMixin, AuthenticationForm, UserCreationForm, \
    UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext as _
from django.contrib.auth import password_validation
from .models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs={'autofocus': True}),
        required = True,
    )

    last_name = forms.CharField(
        label="Cognome",
        widget=forms.TextInput(),
        required=True,
    )

    email = forms.EmailField(
        label="Email",
        error_messages={"invalid": "Perfavore inserisci una email valida"},
        required=True,
    )

    password1 = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    password2 = forms.CharField(
        label="Conferma Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    error_messages = {
        "password_mismatch": _("Le due password non corrispondono."),
    }

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class UserAuthenticatorForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        error_messages={"invalid": "Perfavore inserisci una email valida"},
        widget=forms.EmailInput(attrs={"autofocus": True}),
        required=True,
    )

    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _("La tua email e password non corrispondono. Perfavore prova di nuovo."),
        "inactive": _("Il tuo account è inattivo."),
    }


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(
        label="Nome",
        required=True,
        widget=forms.TextInput()
    )
    last_name = forms.CharField(
        label="Cognome",
        required=True,
        widget=forms.TextInput()
    )
    email = forms.EmailField(
        label="Email",
        error_messages={"invalid": "Perfavore inserisci una email valida"},
        required=True,
    )
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Password Attuale",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password1 = forms.CharField(
        label="Nuova Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        label="Conferma Nuova Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": _(
            "Your old password was entered incorrectly. Please enter it again."
        ),
    }
