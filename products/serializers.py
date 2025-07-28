from rest_framework import serializers
from .models import Product, PricingTier

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class PricingTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingTier
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
