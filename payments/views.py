import os
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .models import PaymentSession

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')  # Amount in dollars
        currency = request.data.get('currency', 'usd')

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {'name': 'Subscription Payment'},
                        'unit_amount': int(float(amount) * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://yourdomain.com/success/',
                cancel_url='https://yourdomain.com/cancel/',
                metadata={'user_id': user.id}
            )

            PaymentSession.objects.create(
                user=user,
                stripe_session_id=session.id,
                amount=amount,
                currency=currency,
                status='pending'
            )

            return Response({'checkout_url': session.url}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            try:
                payment = PaymentSession.objects.get(stripe_session_id=session['id'])
                payment.status = 'success'
                payment.save()
            except PaymentSession.DoesNotExist:
                pass

        return HttpResponse(status=200)
