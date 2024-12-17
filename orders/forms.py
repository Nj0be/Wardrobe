from django import forms

from .models import Order, ReturnItem


class ShippingMethodWidget(forms.RadioSelect):
    option_template_name = "orders/shipping_method_radio_option.html"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone_number", "address_line_one", "address_line_two",
                  "province", "postal_code", "city", "payment_method"]
        labels = {
            "name": "Nome completo (nome e cognome) *",
            "phone_number": "Numero di telefono *",
            "address_line_one": "Riga Indirizzo 1 *",
            "address_line_two": "Riga Indirizzo 2",
            "province": "Provincia *",
            "postal_code": "CAP *",
            "city": "Città *",
            "payment_method": "Metodo di Pagamento"
        }
        widgets = {
            'address_line_one': forms.TextInput(attrs={'placeholder': 'Indirizzo stradale'}),
            'name': forms.TextInput(attrs={'placeholder': 'Nome, cognome, ragione sociale, c/o'}),
            'address_line_two': forms.TextInput(
                attrs={'placeholder': 'Scala, piano, interno, azienda (facoltativo)'}),
            'payment_method': ShippingMethodWidget()
        }


class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = ReturnItem
        fields = ["reason", "comments", "order_item"]
        labels = {
            "reason": "Motivazione del reso *",
            "comments": "Commenti (opzionali)",
        }
        widgets = {
            'reasons': forms.TextInput(attrs={'autocomplete': False}),
            'comments': forms.Textarea(attrs={'rows': 3, 'autocomplete': False}),
            'order_item': forms.HiddenInput(),
        }
