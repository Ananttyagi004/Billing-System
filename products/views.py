from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Product, PricingTier
from .serializers import ProductSerializer, PricingTierSerializer


class ProductListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'detail': 'Only admins can create products.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PricingTierListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tiers = PricingTier.objects.filter(is_active=True)
        serializer = PricingTierSerializer(tiers, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'detail': 'Only admins can create pricing tiers.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PricingTierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductPricingTiersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        tiers = product.tiers.filter(is_active=True)
        serializer = PricingTierSerializer(tiers, many=True)
        return Response(serializer.data)
