from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductUpdateView,
    ProductView,
    # Purchase
    PurchaseCreateView,
    # Sell
    SellCreateView,
)

urlpatterns = [
    path("product_list/", ProductView.as_view(), name="list"),
    path("create/", ProductCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ProductUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="delete"),
    # Purchase
    path("purchase_create/", PurchaseCreateView.as_view(), name="purchase_create"),
    # Sell
    path("sell_create/", SellCreateView.as_view(), name="sell_create"),
]
