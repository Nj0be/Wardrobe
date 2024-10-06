from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("search/", views.search, name="search"),
    path("<int:product_id>/", views.product_page, name="product"),
]
