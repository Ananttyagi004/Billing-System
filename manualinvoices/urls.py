from django.urls import path
from .views import InvoiceParserView

urlpatterns = [
    path('upload/', InvoiceParserView.as_view(), name='upload-manual-invoice'),
]
