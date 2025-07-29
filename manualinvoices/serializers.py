from rest_framework import serializers

class InvoiceUploadSerializer(serializers.Serializer):
    invoice = serializers.FileField()
