from django.db import models


class Category(models.Model):
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
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
    discount_start_date = models.DateTimeField()
    discount_end_date = models.DateTimeField()
    discount_percentage = models.FloatField()

    def __str__(self):
        return f'{self.name}-{self.discount_percentage}%'


class Product(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}-{self.name}'


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True)
    hex = models.CharField(max_length=6, unique=True)

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
    color = models.ForeignKey(ProductColorImage, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [['product', 'color', 'size']]

    def __str__(self):
        return f'{self.product}-{self.color}-{self.size}'