from rest_framework import generics, permissions
from .models import WebhookURL
from .serializers import WebhookURLSerializer

class RegisterWebhookView(generics.CreateAPIView):
    serializer_class = WebhookURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
