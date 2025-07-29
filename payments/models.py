from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_sessions')
    stripe_session_id = models.CharField(max_length=255)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='usd')
    status = models.CharField(max_length=50, default='pending')  # pending, success, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentSession({self.user.email}, {self.status})"
