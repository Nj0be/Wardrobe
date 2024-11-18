from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect

from products.models import ProductVariant
from .forms import PlaceOrderForm
from .models import Order

# TODO
@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user.id).prefetch_related('orderproduct_set')
    return render(request, 'orders/orders_full.html', {'orders': orders})

# TODO
@login_required
def view_order(request, order_id: int):
    order = Order.objects.get(pk=order_id, user=request.user.id)
    return render(request, 'orders/order_full.html', {'order': order})

@login_required
def place(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PlaceOrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlaceOrderForm()


    variants = ProductVariant.objects.filter(cartitem__customer=request.user, cartitem__is_active=True)
    total_price = sum(variant.price or variant.product.price for variant in variants)

    if request.htmx:
        template_name = "orders/place.html",
    else:
        template_name = "orders/place_full.html",

    return render(request, template_name, {"form": form, "variants": variants, "total_price": total_price})
