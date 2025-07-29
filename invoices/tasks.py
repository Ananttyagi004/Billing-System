from .models import Invoice, InvoiceLine
from subscriptions.models import Subscription
from products.models import PricingTier
from taxes.models import TaxRate
from .utils import generate_invoice_pdf
import uuid
from decimal import Decimal

def generate_monthly_invoices():
    subscriptions = Subscription.objects.filter(status='active')

    for sub in subscriptions:
        user = sub.user
        pricing = sub.pricing_tier
        product = pricing.product
        tax_rate = TaxRate.objects.first()  # Or determine based on product

        subtotal = pricing.price
        tax_amount = subtotal * Decimal(tax_rate.rate / 100)
        total = subtotal + tax_amount

        invoice = Invoice.objects.create(
            user=user,
            invoice_number=str(uuid.uuid4()).split('-')[0],
            total_amount=total
        )

        InvoiceLine.objects.create(
            invoice=invoice,
            product=product,
            pricing_tier=pricing,
            quantity=1,
            tax_rate=tax_rate,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total=total
        )

        pdf_path = generate_invoice_pdf(invoice)
        invoice.pdf_file.name = pdf_path.replace("media/", "")
        invoice.save()
