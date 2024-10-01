from django.db.models import Q
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required

from .models import Product, Category, Color, Size, Review


class HomepageView(generic.ListView):
    template_name = "products/homepage.html"
    context_object_name = "main_categories_list"

    def get_queryset(self):
        """Return all the products"""
        return Category.objects.filter(parent_category=None)  # oppure null BOH


def search(request):  # da implementare anche la logica per i filtri
    """ Filtraggio per categoria """

    if request.user.is_authenticated: ## da toglie in production
        auth = True ## da toglie in production
    else: ## da toglie in production
        auth = False ## da toglie in production

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
        products = products.filter(categories__in=selected_category.get_descendants() + [selected_category]).distinct()
    if selected_colors:
        products = products.filter(productvariant__color__in=[selected_color.id for selected_color in selected_colors]).distinct()
    if selected_sizes:
        products = products.filter(productvariant__size__in=[selected_size.id for selected_size in selected_sizes]).distinct()
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
            "auth": auth,  # da toglie in production
        })


def product_page(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    error_message = None
    if request.method == 'POST':
        # review_title = request.POST.get("review_title")
        review_description = request.POST.get("review_description")
        review_vote = request.POST.get("review_vote")

        if request.user.is_authenticated:  # da aggiungere la verifica di acquisto del prodotto da parte dell'utente
            if not Review.objects.filter(product=product, customer=request.user).exists():
                if review_description and review_vote and review_vote.isdigit() and 1 <= int(review_vote) <= 10:  # and review_title
                    review = Review(
                        customer=request.user,
                        product=product,
                        # title=reviewTitle,
                        description=review_description,
                        vote=int(review_vote)
                    )
                    review.save()
                    return redirect('product', product_id=product.id)
                else:
                    error_message = "Dati non validi. Assicurati di compilare correttamente tutti i campi."
            else:
                error_message = "Hai già recensito questo prodotto."
        else:
            error_message = "Devi essere loggato per lasciare una recensione."

    reviews = Review.objects.filter(product=product_id)

    return render(
        request,
        "products/product.html",
        {
            "product": product,
            "reviews": reviews,
            "error_message": error_message,
        })
