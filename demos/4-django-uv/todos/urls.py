from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lists/create/", views.list_create, name="list_create"),
    path("lists/<int:list_id>/", views.list_detail, name="list_detail"),
    path("lists/<int:list_id>/delete/", views.list_delete, name="list_delete"),
    path("lists/<int:list_id>/items/create/", views.item_create, name="item_create"),
    path("lists/<int:list_id>/items/<int:item_id>/toggle/", views.item_toggle, name="item_toggle"),
    path("lists/<int:list_id>/items/<int:item_id>/delete/", views.item_delete, name="item_delete"),
]
