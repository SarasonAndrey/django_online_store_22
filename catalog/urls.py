from django.urls import path

from . import views
from .views import (
    ContactView,
    ProductCreateView,
    ProductDeleteView,
    ProductsByCategoryView,
    ProductUnpublishView,
    ProductUpdateView,
    product_detail,
)

urlpatterns = [
    path("", views.home_view, name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("product/<int:pk>/", product_detail, name="product_detail"),
    path("product/new/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "product/<int:pk>/unpublish/",
        ProductUnpublishView.as_view(),
        name="product_unpublish",
    ),
    path(
        "category/<int:pk>/",
        ProductsByCategoryView.as_view(),
        name="products_by_category",
    ),
]
