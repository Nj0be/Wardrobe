from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.forms.models import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
from products.models import Product, ProductVariant, ProductImage
from django.core.validators import RegexValidator
from django.utils.text import gettext_lazy as _

class Province(models.Model):
    acronym = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f'{self.name}'


class PaymentMethod(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField("Nome completo (nome e cognome)", max_length=40)
    phone_number = PhoneNumberField("Numero di telefono", region="IT")
    address_line_one = models.CharField("Riga Indirizzo 1", max_length=40)
    address_line_two = models.CharField("Riga Indirizzo 2", max_length=40, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    postal_code = models.CharField("CAP", max_length=5, validators = [RegexValidator('^[0-9]{5}$', _('CAP non valido, inserisci 5 numeri'))])
    city = models.CharField("city", max_length=40)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)

    @property
    def total_price(self):
        return sum(product.price * product.quantity for product in OrderProduct.objects.filter(order=self))
    # remove possibility to change order after shipping
    # before shipping it's possible to add OrderProducts to the order and create new payments to pay the OrderProducts
    # the payment class should mark which OrderProducts are paid


class OrderProduct(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, editable=False)
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.PROTECT, editable=False)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    @property
    def name(self):
        return self.variant.product.name

    @property
    def total_price(self):
        return self.price * self.quantity

    @property
    def first_image(self):
        """Returns the first image of the associated product variant."""
        if self.variant and self.variant.product_color:
            product_images = ProductImage.objects.filter(product_color=self.variant.product_color)
            if product_images.exists():
                return product_images.first().image.url  # Return the URL of the first image
        return None  # Return None if no image is found

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.price = self.variant.price or self.variant.product.price

        super(OrderProduct, self).save(*args, **kwargs)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["user", "name", "phone_number", "address_line_one", "address_line_two", "province", "postal_code", "city", "payment_method"]
