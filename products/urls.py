from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name='products/homepage.html'), name="homepage"),
    path("search/", views.search, name="search"),
    path("search/<int:category_id>/", views.search, name="search_category"),
    path("<int:product_id>/", views.product_page, name="product"),
    path("<int:product_id>/<int:color_id>/", views.product_page, name="product_color"),
    path("<int:product_id>/<int:color_id>/", views.product_page, name="product_color"),
    path("<int:product_id>/<int:color_id>/<int:size_id>/", views.product_page, name="product_color_size"),
    path("<int:product_id>/add_review/", views.add_review, name="add_review"),
]
