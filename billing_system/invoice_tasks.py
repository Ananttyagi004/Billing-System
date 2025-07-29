from celery import shared_task
from invoices.models import Invoice
from django.utils.timezone import now
from webhooks.utils import dispatch_webhook_event

@shared_task
def generate_monthly_invoices():
    # Sample logic
    from subscriptions.models import Subscription
    subs = Subscription.objects.filter(is_active=True)
    for sub in subs:
        invoice = Invoice.objects.create(customer=sub.customer, total_amount=sub.pricing_tier.price)
        dispatch_webhook_event(sub.customer.user, 'invoice.generated', {"invoice_id": invoice.id})
