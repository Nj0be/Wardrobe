from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    visible = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    discount_start_date = models.DateTimeField()
    discount_end_date = models.DateTimeField()
    discount_percentage = models.FloatField()

class Category(models.Model):
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    class Meta:
        unique_together = [['parentCategory', 'name']]

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Color(models.Model):
    name = models.CharField(max_length=30, unique=True)
    hex = models.CharField(max_length=6, unique=True)

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

class ProductColorImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, unique=True)
    image = models.CharField(max_length=200)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColorImage, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    class Meta:
        unique_together = [['product', 'color', 'size']]