from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class CartItem(models.Model):
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [['variant', 'user']]

    def clean(self):
        # Don't add product to cart if stock == 0
        self.quantity = min(self.quantity, self.variant.stock)
        if self.quantity == 0:
            raise ValidationError(_("Can't add Product to cart with quantity = 0"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CartItem, self).save(*args, **kwargs)
