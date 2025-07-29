from django.contrib import admin
from .models import PaymentSession

@admin.register(PaymentSession)
class PaymentSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'status', 'created_at')
    search_fields = ('user__email', 'stripe_session_id')
    list_filter = ('status',)
