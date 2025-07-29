from rest_framework import serializers
from .models import WebhookURL

class WebhookURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookURL
        fields = ['id', 'url', 'event_type']
