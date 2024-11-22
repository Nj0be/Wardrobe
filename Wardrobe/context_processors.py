from django.conf import settings

from products.models import Category


def main_categories(request):
    return {
        "MAIN_CATEGORIES": Category.objects.filter(parent=None),
    }
