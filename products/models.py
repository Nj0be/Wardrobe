from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django_extensions.validators import HexValidator


class Category(models.Model):
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = [['parent_category', 'name']]
        verbose_name_plural = "Categories"

    def get_children(self):
        return Category.objects.filter(parent_category=self)

    def get_ancestors(self):
        """
        Metodo ricorsivo per ottenere gli antenati di una categoria
        """

        if self.parent_category is not None:
            ancestors = self.parent_category.get_ancestors()
            ancestors.append(self.parent_category)
            return ancestors
        else:
            return []

    def get_descendants(self):
        """
        Metodo ricorsivo per ottenere tutte le sottocategorie (discendenti)
        """
        descendants = []
        children = self.get_children()
        for child in children:
            descendants.append(child)
            descendants.extend(child.get_descendants())  # Ricorsione per ottenere i figli dei figli
        return descendants

    def __str__(self):
        if self.parent_category:
            return f'{self.parent_category.name}-{self.name}'
        else:
            return f'{self.name}'


class Discount(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    percentage = models.FloatField()

    def __str__(self):
        return f'{self.name}-{self.percentage}%'


class Product(models.Model):
    class VariantType(models.TextChoices):
        NOVARIANT = "NV", _("NoVariant")
        ONLYCOLOR = "OC", _("OnlyColor")
        ONLYSIZE = "OS", _("OnlySize")
        COLORSIZE = "CS", _("ColorSize")

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    variant_type = models.CharField(max_length=2, choices=VariantType, default=VariantType.NOVARIANT)

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(Product, cls).from_db(db, field_names, values)
        # customization to store the original field values on the instance
        instance._loaded_values = dict(
            zip(field_names, (value for value in values if value is not models.DEFERRED))
        )
        return instance

    def save(self, *args, **kwargs):
        # Check how the current values differ from ._loaded_values. For example,
        # prevent changing the variant_type of the model. (This example doesn't
        # support cases where 'variant_type' is deferred).
        if not self._state.adding and (self.variant_type != self._loaded_values["variant_type"]):
            raise ValueError("Updating the value of variant_type isn't allowed")

    def __str__(self):
        return f'{self.id}-{self.name}'


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True)
    hex = models.CharField(max_length=6, unique=True, validators=[HexValidator(length=6)])

    def __str__(self):
        return f'{self.name}'


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.name}'


class ProductColorImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    image = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = [['product', 'color']]

    def __str__(self):
        return f'{self.product}-{self.color}'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColorImage, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.product.variant_type == self.product.VariantType.NOVARIANT:
            if self.color is not None or self.size is not None:
                raise ValidationError("Both Color and Size should be None (Product has no Variant)")
        elif self.product.variant_type == self.product.VariantType.ONLYCOLOR:
            if self.color is None or self.size is not None:
                raise ValidationError("Color shouldn't be None and Size should be None")
        elif self.product.variant_type == self.product.VariantType.ONLYSIZE:
            if self.color is not None or self.size is None:
                raise ValidationError("Color shouldn be None and Size shouldn't be None")
        elif self.product.variant_type == self.product.VariantType.COLORSIZE:
            if self.color is None or self.size is None:
                raise ValidationError("Both Color and Size shouldn't be None")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ProductVariant, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['product', 'color', 'size']]

    def __str__(self):
        return f'{self.product}-{self.color}-{self.size}'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    # title = models.CharField(max_length=100),  # manca il campo in django
    description = models.CharField(max_length=1000)
    vote = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])

    class Meta:
        unique_together = [['product', 'customer']]


class CartItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    def clean(self):
        # Don't add product to cart if stock == 0
        self.quantity = min(self.quantity, self.product_variant.stock)
        if self.quantity == 0:
            raise ValidationError(_("Can't add Product to cart with quantity = 0"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CartItem, self).save(*args, **kwargs)
