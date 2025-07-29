from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_invoice_email(to_email, subject, body):
    send_mail(subject, body, 'invoices@billing.com', [to_email])
