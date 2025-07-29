from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from django.http import FileResponse, Http404

class InvoiceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        invoices = Invoice.objects.filter(user=request.user)
        data = [
            {
                "invoice_number": inv.invoice_number,
                "date": inv.date,
                "total": inv.total_amount,
                "download_url": f"/api/invoices/{inv.id}/download/"
            }
            for inv in invoices
        ]
        return Response(data)


class InvoiceDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk, user=request.user)
            return FileResponse(invoice.pdf_file.open('rb'), content_type='application/pdf')
        except Invoice.DoesNotExist:
            raise Http404("Invoice not found")
