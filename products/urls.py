from django.urls import path
from .views import (
    ProductListCreateView,
    PricingTierListCreateView,
    ProductPricingTiersView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('pricing-tiers/', PricingTierListCreateView.as_view(), name='tier-list-create'),
    path('products/<int:product_id>/tiers/', ProductPricingTiersView.as_view(), name='product-tiers'),
]
