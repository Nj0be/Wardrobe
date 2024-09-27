from django.views import generic
from django.shortcuts import render
from django.http import Http404

from .models import Product, ProductCategory, Category


class HomepageView(generic.ListView):
    template_name = "products/homepage.html"
    context_object_name = "main_categories_list"

    def get_queryset(self):
        """Return all the products"""
        return Category.objects.filter(parent_category=None)  # oppure null BOH


def search(request):  # da implementare anche la logica per i filtri

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

        products = Product.objects.filter(productcategory__category=selected_category.id)
    else:
        ancestors = []
        products = Product.objects.all

    return render(
        request,
        "products/search.html",
        {
            "selected_category": selected_category,
            "root_categories": categories,
            "ancestors": ancestors,
            "products": products,
        })


class ProductView(generic.DetailView):
    model = Product
    template_name = "products/product.html"
