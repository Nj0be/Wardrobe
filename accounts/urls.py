from django.urls import path

from . import views

urlpatterns = [
    path("cipolla/", views.index, name="index"),
]
