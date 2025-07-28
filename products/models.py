from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PricingTier(models.Model):
    INTERVAL_CHOICES = (
        ('one_time', 'One-time'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tiers')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    billing_interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"
