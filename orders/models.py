from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product, ProductVariant, ProductImage


class Order(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    # remove possibility to change order after shipping
    # before shipping it's possible to add OrderProducts to the order and create new payments to pay the OrderProducts
    # the payment class should mark which OrderProducts are paid


class OrderProduct(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = type(ProductVariant._meta.get_field('price'))()

    @property
    def first_image(self):
        """Returns the first image of the associated product variant."""
        if self.product_variant and self.product_variant.product_color:
            product_images = ProductImage.objects.filter(product_color=self.product_variant.product_color)
            if product_images.exists():
                return product_images.first().image.url  # Return the URL of the first image
        return None  # Return None if no image is found

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(OrderProduct, cls).from_db(db, field_names, values)
        # customization to store the original field values on the instance
        instance._loaded_values = dict(
            zip(field_names, (value for value in values if value is not models.DEFERRED))
        )
        return instance

    def clean(self):
        # Don't add product_variant to order if quantity is 0
        if self.quantity > self.product_variant.stock:
            raise ValidationError(_("Can't create OrderProduct: not enough products"))

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.name = self.product_variant.product.name
            self.price = self.product_variant.price or self.product_variant.product.price
        elif self.name != self._loaded_values['name'] or self.price != self._loaded_values['price']:
            raise ValueError("Changing the name or the price of the OrderProduct is not allowed")

        self.full_clean()

        super(OrderProduct, self).save(*args, **kwargs)
