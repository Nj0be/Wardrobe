from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("search/", views.HomepageView.as_view(), name="search"),
    path("search/", views.HomepageView.as_view(), name="search"),
]
