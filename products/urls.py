from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("search/", views.search, name="search"),
    path("<int:pk>/", views.ProductView.as_view(), name="product"),
]
