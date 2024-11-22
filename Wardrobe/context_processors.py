from django.conf import settings

from products.models import Category
from cart.views import Cart

def main_categories(request):
    return {
        "MAIN_CATEGORIES": Category.objects.filter(parent=None),
        "CART_TOTAL_QUANTITY": Cart(request).get_total_quantity(),
    }
