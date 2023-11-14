from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/profile/", views.index, name="index"),
    path("accounts/register/", views.register, name="register"),
    path("search/", views.ArtworkListView.as_view(), name="search"),# # # # # # # # # #
    path("collections/", views.collections, name="collections"),
    path("collection_list/", views.collection_list, name="collection_list"),
    path("collection/add", views.collection_add, name="collection_add"),
    path("collection/edit/<str:name>", views.collection_edit, name="collection_edit"),
    path("collection/artwork/add/<str:artwork_id>/<str:collection_id>", views.collection_artwork_add, name="collection_artwork_add"),
    path("artworks/<str:artwork_id>", views.artwork, name="artwork"),
    path("collections/artworks/<str:artwork_id>", views.artwork, name="artwork"),

]

