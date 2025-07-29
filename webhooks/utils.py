import requests
from .models import WebhookURL, WebhookEventLog

def dispatch_webhook_event(user, event_type, payload):
    webhook_urls = WebhookURL.objects.filter(user=user, event_type=event_type)

    for webhook in webhook_urls:
        try:
            response = requests.post(webhook.url, json=payload, timeout=10)
            WebhookEventLog.objects.create(
                webhook=webhook,
                event_payload=payload,
                status_code=response.status_code,
                response_body=response.text
            )
        except Exception as e:
            WebhookEventLog.objects.create(
                webhook=webhook,
                event_payload=payload,
                status_code=0,
                response_body=str(e)
            )
