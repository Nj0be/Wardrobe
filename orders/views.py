import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect

from cart.models import CartItem
from products.models import ProductVariant
from .forms import OrderForm
from .models import Order, OrderItem


# TODO
@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user.id).prefetch_related('orderitem_set')
    return render(request, 'orders/orders_full.html', {'orders': orders})

# TODO
@login_required
def view_order(request, order_id: int):
    order = Order.objects.prefetch_related('orderitem_set').get(pk=order_id, user=request.user.id)
    return render(request, 'orders/order.html', {'order': order})

# Function not thread safe (if multiple users buy at the same time, bad things can happen)!!
@login_required
def place(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        try:
            product_ids = [int(product_id) for product_id in request.POST.getlist('product_ids')]
            product_prices = [float(price.replace(',', '.')) for price in request.POST.getlist('product_prices')]
            product_quantities = [int(quantity) for quantity in request.POST.getlist('product_quantities')]

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
        form = OrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for product in products:
                # delete objects from cart after order
                CartItem.objects.get(user=request.user, variant=product['variant']).delete()
                # reduce quantity from productvariants after order
                product['variant'].stock -= product['quantity']
                product['variant'].save()
                OrderItem.objects.create(order=order, variant=product['variant'],
                                         quantity=product['quantity'])

            return redirect('view_order', order_id=order.id)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrderForm()
        #variants = ProductVariant.objects.filter(cartitem__user=request.user, cartitem__is_active=True)
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        products = []
        for item in cart_items:
            variant = item.variant
            products.append({'variant': variant, 'quantity': item.quantity,
                             'price': variant.discounted_price, 'subtotal_price': variant.discounted_price*item.quantity})

        if len(products) == 0:
            return redirect('homepage')

    total_price = sum(product['subtotal_price'] for product in products)

    return render(request, 'orders/place.html', {"form": form, "products": products, "total_price": total_price})
