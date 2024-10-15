from django.urls import path
from . import views

urlpatterns = [
    # path('/', views.cart_page, name="cart"),
    path('', views.cart_page, name="cart"),
    path('add/', views.cart_add, name="cart_add"),
    path('edit/', views.cart_edit, name="cart_edit"),
    path('delete/', views.cart_delete, name="cart_delete"),
]
