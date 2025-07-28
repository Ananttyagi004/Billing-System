# subscriptions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import SubscriptionSerializer
from products.models import PricingTier

class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pricing_tier_id = request.data.get('pricing_tier')
        if not pricing_tier_id:
            return Response({'error': 'pricing_tier is required'}, status=400)

        try:
            tier = PricingTier.objects.get(id=pricing_tier_id)
        except PricingTier.DoesNotExist:
            return Response({'error': 'Invalid pricing_tier ID'}, status=404)

        subscription = Subscription.objects.create(
            user=request.user,
            pricing_tier=tier,
            product=tier.product,
        )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, subscription_id):
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=request.user)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription not found'}, status=404)

        if not subscription.is_active:
            return Response({'message': 'Subscription already cancelled'}, status=400)

        subscription.cancel()
        return Response({'message': 'Subscription cancelled successfully'}, status=200)

class ListSubscriptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
