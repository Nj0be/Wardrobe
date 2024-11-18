from django import forms
from django.core.validators import RegexValidator
from django.utils.text import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from orders.models import Province, PaymentMethod


class ShippingMethodWidget(forms.RadioSelect):
    option_template_name = "orders/shipping_method_radio_option.html"


class PlaceOrderForm(forms.Form):
    name = forms.CharField(
        label = "Nome completo (nome e cognome) *",
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'Nome, cognome, ragione sociale, c/o'}),
        required = True,
    )

    phone_number = PhoneNumberField(
        label = "Numero di telefono *",
        region="IT",
        required=True
    )

    address_line_one = forms.CharField(
        label = "Riga Indirizzo 1 *",
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'Indirizzo stradale'}),
        required = True,
    )

    address_line_two = forms.CharField(
        label = "Riga Indirizzo 2",
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'Scala, piano, interno, azienda (facoltativo)'}),
        required = False,
    )

    province = forms.ModelChoiceField(
        label = "Provincia *",
        queryset = Province.objects,
        initial = '0',
        required = True,
    )

    postal_code = forms.CharField(
        label = "CAP *",
        max_length=5,
        validators=[RegexValidator('^[0-9]{5}$', _('CAP non valido, inserisci 5 numeri'))],
        required = True,
    )

    city = forms.CharField(
        label = "Città *",
        max_length=40,
        required = True,
    )

    payment_method = forms.ModelChoiceField(
        label = "Metodo di Pagamento",
        # choices = ((0, "Contrassegno"), (1, "Paypal"), (2, "Stripe")),
        queryset = PaymentMethod.objects,
        # coerce = lambda x: bool(int(x)),
        widget = ShippingMethodWidget(),
        initial = '0',
        required = True,
    )
