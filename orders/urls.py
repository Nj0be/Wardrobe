from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_orders, name="view_orders"),
    path("<int:order_id>/", views.view_order, name="view_order"),
    path('place/', views.place, name="place_order"),
]
