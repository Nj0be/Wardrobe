from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product, ProductVariant, ProductImage


class Province(models.Model):
    acronym = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50, unique=True)


class Order(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    # remove possibility to change order after shipping
    # before shipping it's possible to add OrderProducts to the order and create new payments to pay the OrderProducts
    # the payment class should mark which OrderProducts are paid


class OrderProduct(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, editable=False)
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.PROTECT, editable=False)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    @property
    def first_image(self):
        """Returns the first image of the associated product variant."""
        if self.product_variant and self.product_variant.product_color:
            product_images = ProductImage.objects.filter(product_color=self.product_variant.product_color)
            if product_images.exists():
                return product_images.first().image.url  # Return the URL of the first image
        return None  # Return None if no image is found

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.price = self.product_variant.price or self.product_variant.product.price

        super(OrderProduct, self).save(*args, **kwargs)
