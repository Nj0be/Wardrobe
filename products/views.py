from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import HttpResponseNotFound, Http404
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductVariant, ProductColor, Category, Color, Size, Review, \
    ProductImage, Brand


class HomepageView(generic.ListView):
    template_name = "products/homepage.html"
    context_object_name = "main_categories_list"

    def get_queryset(self):
        """Return all the products"""
        return Category.objects.filter(parent=None)  # oppure null BOH


def search(request, category_id=None):  # da implementare anche la logica per i filtri
    """ Filtraggio per categoria """
    if request.method != "GET":
        return HttpResponseNotFound('<h1>Page not found</h1>')


    """ Selezione prodotti """
    # selezioniamo solo i prodotto che hanno almeno una product variant
    selected_category = Category.objects.filter(id=category_id).first()
    products = Product.objects.filter(is_active=True ,productcolor__productvariant__isnull=False).distinct()
    if selected_category:
        categories = [selected_category.parent] + list(selected_category.children.all())
        products = products.filter(categories__in=selected_category.descendants(include_self=True))
    else:
        # get 'root' categories (first layer)
        categories = Category.objects.with_tree_fields().extra(where=["__tree.tree_depth <= %s"], params=[0])

    """ Filtraggio per ricerca testuale """
    search_terms = request.GET.get('search_terms', None)
    if search_terms and len(search_terms) > 2:
        # get words with len > 2 and create query for postgres search ( word1:* & word2:* & etc...)
        query_str = ' & '.join([w+':*' for w in search_terms.split() if len(w) > 2])
        vector = (SearchVector('name', weight='A', config='italian') +
                  SearchVector('description', weight='B', config='italian') +
                  SearchVector('brand__name', weight='B', config='italian') +
                  SearchVector('categories_names', weight='C', config='italian') +
                  SearchVector('productcolor__color_names', weight='C', config='italian'))
        query = SearchQuery(query_str, search_type="raw", config='italian')
        # query = SearchQuery(search_terms, config='italian')
        products = products.annotate(
            categories_names=ArrayAgg('categories__name'),
            productcolor__color_names=ArrayAgg("productcolor__color__name"),
            rank=SearchRank(vector, query), search=vector).filter(rank__gte=0.1).order_by('-rank')
        # rank = SearchRank(vector, query), search = vector).filter(search=search_terms).order_by('-rank')

    """ Filtraggio per marca """
    brands = Brand.objects.filter(product__in=list(products)).distinct().order_by('-name')
    selected_brands = brands.filter(pk__in=request.GET.getlist('brand', None))
    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    """ Filtraggio per colori """
    colors = Color.objects.filter(productcolor__product__in=list(products)).distinct().order_by('-hex')
    selected_colors = colors.filter(pk__in=request.GET.getlist('color', None))
    if selected_colors:
        products = products.filter(productcolor__color__in=selected_colors)

    """ Filtraggio per taglie """
    sizes = Size.objects.filter(productvariant__product_color__product__in=list(products)).distinct().order_by('position')
    selected_sizes = sizes.filter(pk__in=request.GET.getlist('size', None))
    if selected_sizes:
        products = products.filter(productcolor__productvariant__size__id__in=selected_sizes)

    if request.htmx:
        template_name = "products/search.html",
    else:
        template_name = "products/search_full.html",

    """ Invia la risposta """
    return render(
        request,
        template_name,
        {
            "categories": categories,
            "selected_category": selected_category,
            "brands": brands,
            "selected_brands": selected_brands,
            "colors": colors,
            "selected_colors": selected_colors,
            "sizes": sizes,
            "selected_sizes": selected_sizes,
            "search_terms": search_terms,
            "products": products,
        })


def product_page(request, product_id, color_id=None, size_id=None):
    if request.method != "GET":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    product = get_object_or_404(Product, pk=product_id, is_active=True)
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
                                             product_color__color_id=color_id)

    if not size_id and len(variants) == 1 and variants[0].stock > 0:
        return redirect('product_color_size', product_id=product_id, color_id=color_id,
                        size_id=variants[0].size.id)

    # we consider only available sizes
    selected_size = Size.objects.filter(productvariant__product_color=product_color, id=size_id,
                                        productvariant__stock__gt=0).first()
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
    size_variants = {size: None for size in sizes} | {variant.size: variant for variant in variants
                                                      if variant.stock}

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

    # if request come from htmx-boost, send full page
    if request.htmx and not request.htmx.boosted:
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
