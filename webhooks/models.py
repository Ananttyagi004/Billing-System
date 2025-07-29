from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WebhookURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    event_type = models.CharField(max_length=100)  # e.g. invoice.generated, payment.success
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} → {self.event_type}"

class WebhookEventLog(models.Model):
    webhook = models.ForeignKey(WebhookURL, on_delete=models.CASCADE)
    event_payload = models.JSONField()
    status_code = models.IntegerField()
    response_body = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.id} – {self.webhook.event_type}"
s