import os
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings

def generate_invoice_pdf(invoice):
    html_string = render_to_string("invoices/invoice_template.html", {"invoice": invoice})
    html = HTML(string=html_string)
    pdf_path = f"media/invoices/pdfs/invoice_{invoice.invoice_number}.pdf"
    html.write_pdf(pdf_path)
    return pdf_path
