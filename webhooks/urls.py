from django.urls import path
from .views import RegisterWebhookView

urlpatterns = [
    path('register/', RegisterWebhookView.as_view(), name='webhook-register'),
]
