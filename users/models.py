from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    billing_email = models.EmailField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"
