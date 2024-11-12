from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.conf import settings
from cart.models import CartItem
from products.models import ProductVariant
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

class Cart:
    def __init__(self, request):
        request.session.modified = True
        self.user = request.user
        if not request.session.get(settings.CART_SESSION_ID):
            request.session[settings.CART_SESSION_ID] = {}
        self.session_cart = request.session[settings.CART_SESSION_ID]
        self.cart = {}

        for variant_id, attr in list(self.session_cart.items()):
            try:
                variant = ProductVariant.objects.get(id=variant_id,
                                                     product_color__product__is_active=True)
                quantity = int(attr['quantity'])
                is_active = bool(attr['is_active'])
            except (ObjectDoesNotExist, ValueError, TypeError) as e:
                del self.session_cart[variant_id]
                continue
            if self.user.is_authenticated:
                # if user is authenticated, remove everything from session cookie and create objects in db
                self[variant] += quantity
                del self.session_cart[variant_id]
            else:
                self.cart[variant] = self.session_cart[variant_id]

    def __setitem__(self, variant: ProductVariant, quantity: int):
        if not isinstance(variant, ProductVariant):
            raise TypeError("variant argument is not a ProductVariant")
        if not isinstance(quantity, int):
            raise TypeError("quantity argument is not an int")

        variant_id = str(variant.id)

        if quantity > variant.stock:
            quantity = variant.stock

        if quantity == 0:
            del self[variant]
            return

        if self.user.is_authenticated:
            try:
                item = CartItem.objects.get(product_variant=variant, customer=self.user)
                item.quantity = quantity
                item.save()
            except ObjectDoesNotExist:
                CartItem.objects.create(product_variant=variant, customer=self.user, quantity=quantity)
        else:
            if variant not in self.cart:
                self.cart[variant] = {}
                self.session_cart[variant_id] = {}
            self.cart[variant]['quantity'] = quantity
            self.cart[variant]['is_active'] = True
            self.session_cart[variant_id] = self.cart[variant]

    def __getitem__(self, variant: ProductVariant):
        if not isinstance(variant, ProductVariant):
            raise TypeError("variant argument is not a ProductVariant")

        if self.user.is_authenticated:
            item = CartItem.objects.filter(product_variant=variant, customer=self.user).first()
            if item:
                return item.quantity
            else:
                return 0
        else:
            item = self.cart.get(variant, None)
            if item:
                return self.cart[variant]['quantity']
            else:
                return 0

    def __delitem__(self, variant: ProductVariant):
        if not isinstance(variant, ProductVariant):
            raise TypeError("variant argument is not a ProductVariant")

        if self.user.is_authenticated:
            try:
                CartItem.objects.get(product_variant=variant, customer=self.user).delete()
            except ObjectDoesNotExist:
                pass
        else:
            variant_id = str(variant.id)
            del self.cart[variant]
            del self.session_cart[variant_id]

    def __iter__(self):
        if self.user.is_authenticated:
            yield from CartItem.objects.filter(customer=self.user)
        else:
            yield from self.cart

    def set_is_active(self, variant: ProductVariant, is_active: bool):
        if not isinstance(variant, ProductVariant):
            raise TypeError("variant argument is not a ProductVariant")
        if not isinstance(is_active, bool):
            raise TypeError("quantity argument is not a bool")

        if self.user.is_authenticated:
            try:
                item = CartItem.objects.filter(product_variant=variant, customer=self.user).first()
                item.is_active = is_active
                item.save()
            except:
                raise ValueError(f"User {self.user.id} doesn't have variant {variant.id} in the cart")
        else:
            self[variant]['is_active'] = is_active

    def enable(self, variant: ProductVariant):
        self.set_is_active(variant, True)

    def disable(self, variant: ProductVariant):
        self.set_is_active(variant, False)

    def values(self):
        return self.session_cart.values()

    def keys(self):
        return self.session_cart.keys()

    def items(self):
        if self.user.is_authenticated:
            cart = {}
            for item in CartItem.objects.filter(customer=self.user):
                variant = item.product_variant
                cart[variant] = {}
                cart[variant]['quantity'] = item.quantity
                cart[variant]['is_active'] = item.is_active
            return cart.items()
        else:
            return self.cart.items()

    def __len__(self):
        return len(self.session_cart)


# create cart on login to transfer cartitems from session to db
@receiver(user_logged_in)
def login_handler(sender, user, request, **kwargs):
    Cart(request)


def cart_page(request):
    cart = Cart(request)

    if request.htmx:
        template_name = "cart/cart.html",
    else:
        template_name = "cart/cart_full.html",

    return render(
        request,
        template_name,
        {
            "cart": cart,
        }
    )


def cart_edit(request):
    if request.method != "POST" or not request.htmx:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    try:
        variant_id = request.POST['variant_id']
        variant = ProductVariant.objects.get(id=variant_id, product_color__product__is_active=True)
    except KeyError:
        return HttpResponseBadRequest("missing product variant")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("product variant doesn't exists")

    cart = Cart(request)

    if 'quantity' in request.POST:
        try:
            quantity = int(request.POST['quantity'])
            cart[variant] = quantity
        except TypeError:
            return HttpResponseBadRequest("quantity argument is not an int")
        except Exception as e:
            return HttpResponseBadRequest(e)

    if 'is_active' in request.POST:
        try:
            is_active = bool(request.POST['is_active'])
            cart.set_is_active(variant, is_active)
        except TypeError:
            return HttpResponseBadRequest("is_active argument is not a bool")
        except Exception as e:
            return HttpResponseBadRequest(e)

    return HttpResponse("")


def cart_delete(request):
    if request.method != "POST" or not request.htmx:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    try:
        variant_id = request.POST['variant_id']
        variant = ProductVariant.objects.get(id=variant_id, product_color__product__is_active=True)
    except KeyError:
        return HttpResponseBadRequest("missing product variant")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("product variant doesn't exists")

    cart = Cart(request)
    try:
        del cart[variant]
    except Exception as e:
        return HttpResponseBadRequest(e)

    return HttpResponse("")


def cart_add(request):
    if request.method != "POST" or not request.htmx:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    try:
        variant_id = request.POST['variant_id']
        variant = ProductVariant.objects.get(id=variant_id, product_color__product__is_active=True)
    except KeyError:
        return HttpResponseBadRequest("missing product variant")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("product variant doesn't exists")

    cart = Cart(request)

    try:
        quantity = int(request.POST['quantity'])
        cart[variant] += quantity
    except TypeError:
        return HttpResponseBadRequest("quantity argument is not an int")
    except Exception as e:
        return HttpResponseBadRequest(e)

    return render(
        request,
        "cart/cart_add.html"
    )
