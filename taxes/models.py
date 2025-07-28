from django.db import models

class TaxRate(models.Model):
    name = models.CharField(max_length=100)  # e.g., GST, VAT, Service Tax
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 18.00
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"