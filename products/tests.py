from django.test import TestCase
from .models import Product, Brand, Review, Decimal
from accounts.models import User


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
        product_name = product.name
        self.assertEqual(product_name, 'productName')

    def test_description(self):
        product = Product.objects.get(id=1)
        product_description = product.description
        self.assertEqual(product_description, 'productDescription')

    def test_price(self):
        product = Product.objects.get(id=1)
        product_price = product.price
        self.assertEqual(product_price, Decimal('0.01'))

    def test_object_name_is_id_and_name(self):
        product = Product.objects.get(id=1)
        expected_object_name = f'{product.id}-{product.name}'
        self.assertEqual(str(product), expected_object_name)


class ReviewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Review.objects.create(
            product=Product.objects.create(
                name="productName",
                price=Decimal('0.01'),
                brand=Brand.objects.create(name="BrandName")
            ),
            user=User.objects.create(
                email='hello@world.com',
                first_name='hello',
                last_name='world'
            ),
            title="reviewTitle",
            description="reviewDescription",
            vote=1,
        )

    def test_product(self):
        review = Review.objects.get(id=1)
        product_name = review.product.name
        self.assertEqual(product_name, 'productName')

    def test_title(self):
        review = Review.objects.get(id=1)
        review_title = review.title
        self.assertEqual(review_title, 'reviewTitle')

    def test_description(self):
        review = Review.objects.get(id=1)
        review_description = review.description
        self.assertEqual(review_description, 'reviewDescription')

    def test_vote(self):
        review = Review.objects.get(id=1)
        review_vote = review.vote
        self.assertEqual(review_vote, 1)
