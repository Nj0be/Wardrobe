from django.views import generic
from .models import Product


"""
def homepage(request):
    products_list = Product.objects.all()
    return render(request, "products/homepage.html", {"products_list": products_list})
"""
class HomepageView(generic.ListView):
    template_name = "products/homepage.html"
    context_object_name = "products_list"

    def get_queryset(self):
        """Return all the products"""
        return Product.objects.all()

class SearchView(generic.ListView): # mancano i filtri passati come parametri
    template_name = "products/search.html"
    context_object_name = "products_list"

    # Manca la logica di filtraggio

    def get_queryset(self):
        """Return all the products."""
        return Product.objects.all()

class ProductView(generic.DetailView):
    model = Product
    template_name = "products/product.html"