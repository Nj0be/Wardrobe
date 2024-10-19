from tree_queries.models import TreeNode
from django.db import models
from django.core.validators import MaxValueValidator
from django_extensions.validators import HexValidator
from cart.models import CartItem


class Category(TreeNode):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']
        unique_together = [['parent', 'name']]
        verbose_name_plural = "Categories"

    def _set_parent(self, parent):
        # Method used for moving categories in admin panel
        self.parent = parent

    def __str__(self):
        parent_category = self.parent
        parent_str = ''
        while parent_category:
            parent_str += f'{parent_category.name}-'
            parent_category = parent_category.parent
        return parent_str + f'{self.name}'


class Discount(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    percentage = models.FloatField()

    def __str__(self):
        return f'{self.name}-{self.percentage}%'
    
    
class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def has_variants(self):
        return len(ProductVariant.objects.filter(product_color__product=self)) > 0

    def save(self, *args, **kwargs):
        super(Product, self).save(args, kwargs)
        if not self.is_active:
            CartItem.objects.filter(product_variant__product_color__product=self).delete()

    def __str__(self):
        return f'{self.id}-{self.name}'


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True)
    hex = models.CharField(max_length=6, unique=True, validators=[HexValidator(length=6)])

    def __str__(self):
        return f'{self.name}'


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)
    position = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.name}'


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def get_images(self):
        return [prod_image.image for prod_image in ProductImage.objects.filter(product_color=self)]

    class Meta:
        unique_together = [['product', 'color']]

    def __str__(self):
        return f'{self.product}-{self.color}'


class ProductImage(models.Model):
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    class Meta:
        unique_together = [['product_color', 'image']]

    def __str__(self):
        return f'{self.product_color.product}-{self.product_color.color}-{self.image}'


class ProductVariant(models.Model):
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    stock = models.PositiveIntegerField()

    def is_active(self):
        return self.product_color.product.is_active

    def get_images(self):
        return self.product_color.get_images()

    @property
    def product(self):
        return self.product_color.product

    @property
    def color(self):
        return self.product_color.color

    class Meta:
        unique_together = [['product_color', 'size']]

    def __str__(self):
        return f'{self.product}-{self.color}-{self.size}'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    vote = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])

    class Meta:
        unique_together = [['product', 'customer']]

