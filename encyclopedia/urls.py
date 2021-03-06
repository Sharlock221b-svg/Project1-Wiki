from unicodedata import name
from django.urls import path
from . import views

#declaring the app_name helps in refering to the specific url
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.getPage, name="getPage"),
    path("wiki/new", views.newPage, name="newPage"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/random", views.Random, name="random")
]
