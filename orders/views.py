import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect

from cart.models import CartItem
from products.models import ProductVariant
from .forms import PlaceOrderForm
from .models import Order, OrderProduct


# TODO
@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user.id).prefetch_related('orderproduct_set')
    return render(request, 'orders/orders_full.html', {'orders': orders})

# TODO
@login_required
def view_order(request, order_id: int):
    order = Order.objects.prefetch_related('orderproduct_set').get(pk=order_id, user=request.user.id)
    return render(request, 'orders/order.html', {'order': order})

# Function not thread safe (if multiple users buy at the same time, bad things can happen)!!
@login_required
def place(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        try:
            product_ids = list(map(int, request.POST.getlist('product_ids')))
            product_prices = list(map(float, request.POST.getlist('product_prices')))
            product_quantities = list(map(int, request.POST.getlist('product_quantities')))

            products = []
            for (product_id, price, quantity) in zip(product_ids, product_prices, product_quantities):
                variant = ProductVariant.objects.get(pk=product_id)
                products.append({'variant': variant, 'quantity': quantity,
                             'price': price, 'subtotal_price': price*quantity})
            # variants = ProductVariant.objects.filter(id__in=variants)
        except KeyError:
            return redirect('cart')

        if len(products) == 0:
            return redirect('homepage')
        # create a form instance and populate it with data from the request:
        form = PlaceOrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            order = Order.objects.create(user=request.user, name=form.cleaned_data['name'],
                                         phone_number=form.cleaned_data['phone_number'],
                                         address_line_one=form.cleaned_data['address_line_one'],
                                         address_line_two=form.cleaned_data['address_line_two'],
                                         province=form.cleaned_data['province'],
                                         postal_code=form.cleaned_data['postal_code'],
                                         city=form.cleaned_data['city'],
                                         payment_method=form.cleaned_data['payment_method'])
            for product in products:
                # delete objects from cart after order
                CartItem.objects.get(customer=request.user, variant=product['variant']).delete()
                # reduce quantity from productvariants after order
                product['variant'].stock -= product['quantity']
                product['variant'].save()
                OrderProduct.objects.create(order=order, variant=product['variant'],
                                            quantity=product['quantity'], price=product['price'])

            return redirect('view_order', order_id=order.id)
        import sys
        print(form.errors, file=sys.stderr)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlaceOrderForm()
        #variants = ProductVariant.objects.filter(cartitem__customer=request.user, cartitem__is_active=True)
        cart_items = CartItem.objects.filter(customer=request.user, is_active=True)

        products = []
        for item in cart_items:
            variant = item.variant
            products.append({'variant': variant, 'quantity': item.quantity,
                             'subtotal_price': variant.real_price*item.quantity})

        if len(products) == 0:
            return redirect('homepage')

    total_price = sum(product['subtotal_price'] for product in products)

    return render(request, 'orders/place.html', {"form": form, "products": products, "total_price": total_price})
