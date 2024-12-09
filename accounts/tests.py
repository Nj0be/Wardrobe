from django.test import TestCase
from .models import User


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(email='hello@world.com', first_name='hello', last_name='world')

    def test_email(self):
        user = User.objects.get(id=1)
        field_label = user.email
        self.assertEqual(field_label, 'hello@world.com')

    def test_object_name_is_email(self):
        user = User.objects.get(id=1)
        expected_object_name = f'{user.email}'
        self.assertEqual(str(user), expected_object_name)
