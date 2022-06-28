from unicodedata import name
from django.urls import path
from . import views

#declaring the app_name helps in refering to the specific url
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.getPage, name="getPage"),
]
