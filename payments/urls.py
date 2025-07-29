from django.urls import path
from .views import InitiatePaymentView, StripeWebhookView

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
