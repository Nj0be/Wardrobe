from django.db.models import Q
from django.views import generic
from django.shortcuts import render

from .models import Product, Category, Color, Size


class HomepageView(generic.ListView):
    template_name = "products/homepage.html"
    context_object_name = "main_categories_list"

    def get_queryset(self):
        """Return all the products"""
        return Category.objects.filter(parent_category=None)  # oppure null BOH


def search(request):  # da implementare anche la logica per i filtri

    """ Filtraggio per categoria """

    selected_category_id = int(request.GET.get('category')) if request.GET.get('category') else None

    if selected_category_id:
        # viene passato un id di una categoria tra i parametri
        try:
            # nel caso il valore dell'id è presente nel db
            selected_category = Category.objects.get(pk=selected_category_id)
        except Category.DoesNotExist:
            selected_category = None
    else:
        selected_category = None

    categories = Category.objects.filter(parent_category__isnull=True)

    if selected_category is not None:
        ancestors = selected_category.get_ancestors()
        ancestors.append(selected_category)
    else:
        ancestors = []

    """ Filtraggio per ricerca testuale """

    search_terms = request.GET.get('search_terms') if request.GET.get('search_terms') else None

    """ Filtraggio per colori """

    selected_colors_ids = request.GET.getlist('color')
    selected_colors = []
    for selected_color_id in selected_colors_ids:
        try:
            selected_colors.append(Color.objects.get(pk=selected_color_id))
        except Color.DoesNotExist:
            pass
    colors = Color.objects.all()

    """ Filtraggio per taglie """

    selected_sizes_ids = request.GET.getlist('size')
    selected_sizes = []
    for selected_size_id in selected_sizes_ids:
        try:
            selected_sizes.append(Size.objects.get(pk=selected_size_id))
        except Size.DoesNotExist:
            pass
    sizes = Size.objects.all()

    """ Selezione prodotti """
    products = Product.objects.all()

    if selected_category:
        products = products.filter(productcategory__category__in=[descendant.id for descendant in selected_category.get_descendants() + [selected_category]])
    if selected_colors:
        products = products.filter(productvariant__color__in=[selected_color.id for selected_color in selected_colors])
    if selected_sizes:
        products = products.filter(productvariant__size__in=[selected_size.id for selected_size in selected_sizes])
    if search_terms:
        # check if title contains any of the strings in the search_terms list
        query = Q()
        keywords = search_terms.split(" ")
        for keyword in keywords:
            query |= Q(name__icontains=keyword)
        products = products.filter(query)

    """ Invia la risposta """
    return render(
        request,
        "products/search.html",
        {
            "selected_category": selected_category,
            "root_categories": categories,
            "ancestors": ancestors,
            "products": products,
            "colors": colors,
            "selected_colors": selected_colors,
            "sizes": sizes,
            "selected_sizes": selected_sizes,
            "search_terms": search_terms,
        })


class ProductView(generic.DetailView):
    model = Product
    template_name = "products/product.html"
