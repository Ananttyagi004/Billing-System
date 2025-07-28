from django.db import models
from django.contrib.auth.models import User
from products.models import PricingTier, Product
from django.utils import timezone

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    pricing_tier = models.ForeignKey(PricingTier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def cancel(self):
        self.is_active = False
        self.auto_renew = False
        self.cancelled_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.pricing_tier.name}"