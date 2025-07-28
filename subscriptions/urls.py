
from django.urls import path
from .views import (
    CreateSubscriptionView,
    CancelSubscriptionView,
    ListSubscriptionsView
)

urlpatterns = [
    path('subscriptions/', ListSubscriptionsView.as_view(), name='subscription-list'),
    path('subscriptions/create/', CreateSubscriptionView.as_view(), name='subscription-create'),
    path('subscriptions/<int:subscription_id>/cancel/', CancelSubscriptionView.as_view(), name='subscription-cancel'),
]
