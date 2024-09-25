from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<int:pk>/", views.ProductView.as_view(), name="product"),
]
