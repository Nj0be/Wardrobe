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
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = [['parent_category', 'name']]

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
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    image = models.CharField(max_length=200)

    class Meta:
        unique_together = [['product', 'color']]


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColorImage, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [['product', 'color', 'size']]