from django.urls import path
from .views import TaxRateCreateView, TaxRateListView

urlpatterns = [
    path('tax-rates/', TaxRateListView.as_view(), name='tax-rate-list'),
    path('tax-rates/create/', TaxRateCreateView.as_view(), name='tax-rate-create'),
]
