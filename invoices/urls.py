from django.urls import path
from .views import InvoiceListView, InvoiceDownloadView

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice-list'),
    path('<int:pk>/download/', InvoiceDownloadView.as_view(), name='invoice-download'),
]
