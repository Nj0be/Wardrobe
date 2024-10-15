from django.db.models import Q
from django.http import HttpResponseNotFound, Http404
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductVariant, ProductColor, Category, Color, Size, Review, ProductImage


class HomepageView(generic.ListView):
    template_name = "products/homepage.html"
    context_object_name = "main_categories_list"

    def get_queryset(self):
        """Return all the products"""
        return Category.objects.filter(parent_category=None)  # oppure null BOH


def search(request):  # da implementare anche la logica per i filtri
    """ Filtraggio per categoria """

    if request.method == "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

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
        products = products.filter(productcolor__color__in=selected_colors).distinct()
    if selected_sizes:
        products = products.filter(productcolor__productvariant__size__in=selected_sizes).distinct()
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


def product_page(request, product_id, color_id=None, size_id=None):
    product = get_object_or_404(Product, pk=product_id)
    price = product.price
    stock = 0

    # if product doesn't have variants, it can't be displayed
    if not product.has_variants():
        raise Http404()

    colors = Color.objects.filter(productcolor__product_id=product_id)
    color_id = color_id or colors[0].id


    selected_color = Color.objects.filter(id=color_id, productcolor__product_id=product_id).first()
    if color_id and not selected_color:
        return redirect('product', product_id=product_id)

    product_color = ProductColor.objects.get(product=product_id, color=selected_color)
    variants = ProductVariant.objects.filter(product_color__product=product,
                                             product_color__color_id=color_id,
                                             is_active=True)


    # we consider only available sizes
    selected_size = Size.objects.filter(productvariant__product_color=product_color, id=size_id, productvariant__stock__gt=0).first()
    if size_id and not selected_size:
        return redirect('product_color', product_id=product_id, color_id=color_id)

    if selected_size:
        price = variants.filter(size=selected_size).first().price or price
        stock = variants.get(size_id=selected_size).stock

    sizes = Size.objects.filter(productvariant__product_color__product=product_id).distinct()

    images = ProductImage.objects.filter(
        product_color=product_color
    )

    # second one take priority
    size_variants = {size: None for size in sizes} | {variant.size: variant for variant in variants if variant.stock}

    # Review logic
    error_message = None
    if request.method == 'GET':
        # review_title = request.GET.get("review_title")
        review_description = request.GET.get("review_description")
        review_vote = request.GET.get("review_vote")

        if review_description and review_vote and review_vote.isdigit() and 1 <= int(
                review_vote) <= 10:  # and review_title
            if request.user.is_authenticated:  # da aggiungere la verifica di acquisto del prodotto da parte dell'utente
                if not Review.objects.filter(product=product, customer=request.user).exists():
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
                    error_message = "Hai già recensito questo prodotto."
            else:
                error_message = "Devi aver eseguito il login per lasciare una recensione."

    reviews = Review.objects.filter(product=product_id)

    if request.htmx:
        template_name = "products/product.html",
    else:
        template_name = "products/product_full.html",

    return render(
        request,
        template_name,
        {
            "product": product,
            "colors": colors,
            "selected_color": selected_color,
            "selected_size": selected_size,
            "images": images,
            "size_variants": size_variants,
            "price": price,
            "reviews": reviews,
            "error_message": error_message,
            "stock": stock,
        }
    )
