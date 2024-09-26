from django.views import generic
from django.shortcuts import render

from .models import Product
from .models import Category


class HomepageView(generic.ListView):
    template_name = "products/homepage.html"
    context_object_name = "main_categories_list"

    def get_queryset(self):
        """Return all the products"""
        return Category.objects.filter(parent_category=0)  # oppure null BOH


# nell'url non prende nessun argomento attualmente... too bad (missing 5 required positional arguments)
def search(request, category, colors, sizes, price_range, search_term):
    # quando la pagina di ricerca viene chiamata dall'homepage, solamente category è non nulla
    # verrà settata come una tra quelle con parent_id = 0 in quanto nella homepage verranno mostrate solo le copertine
    # delle master category (product_id=0)

    # LEGGERE IL README PER CAPIRE COME AFFRONTARE LA RICORSIONE DELLE CATEGORIE

    # Manca la logica di filtraggio dei prodotti
    # i filtri dovrebbero andare a lavorare sulle tabelle: productVariant, productColor etc per ridare i prodotti che \
    # rispecchiano quelle info

    products_list = Product.objects.all()

    return render(  # da cambiare
        request,
        "products/search.html",
        {
            "products_list": products_list,
            "category": category,
            "colors": colors,
            "sizes": sizes,
            "price_range": price_range,
            "search_query": search_term
        })


class ProductView(generic.DetailView):
    model = Product
    template_name = "products/product.html"
