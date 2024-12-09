from django.test import TestCase
from .models import Product, Brand, Decimal


class ProductTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Product.objects.create(name="productName",
                               price=Decimal('0.01'),
                               description="productDescription",
                               brand=Brand.objects.create(name="BrandName")
                               )

    def test_name(self):
        product = Product.objects.get(id=1)
        field_label = product.name
        self.assertEqual(field_label, 'productName')

    def test_description(self):
        product = Product.objects.get(id=1)
        field_label = product.description
        self.assertEqual(field_label, 'productDescription')

    def test_price(self):
        product = Product.objects.get(id=1)
        field_label = product.price
        self.assertEqual(field_label, Decimal('0.01'))

    def test_object_name_is_id_and_name(self):
        product = Product.objects.get(id=1)
        expected_object_name = f'{product.id}-{product.name}'
        self.assertEqual(str(product), expected_object_name)
