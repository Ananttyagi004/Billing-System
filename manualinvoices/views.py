from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os

from .serializers import InvoiceUploadSerializer
from .utils import convert_pdf_to_images
from textract_service import TextractInvoiceExtractor
from .models import ManualInvoice


@method_decorator(csrf_exempt, name='dispatch')
class InvoiceParserView(GenericAPIView):
    serializer_class = InvoiceUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['invoice']

            valid_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            if file_extension not in valid_extensions:
                return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

            invoice_directory = os.path.join(settings.MEDIA_ROOT, 'manual_invoices', 'uploads')
            os.makedirs(invoice_directory, exist_ok=True)
            file_path = os.path.join(invoice_directory, uploaded_file.name)

            with open(file_path, "wb") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            textract_service = TextractInvoiceExtractor()
            try:
                extracted_data = textract_service.extract_data(file_path)
            except textract_service.client.exceptions.UnsupportedDocumentException:
                image_paths = convert_pdf_to_images(file_path)
                extracted_data = {"key_fields": {}, "line_items": []}
                for img_path in image_paths:
                    image_data = textract_service.extract_data(img_path)
                    extracted_data['key_fields'].update(image_data['key_fields'])
                    extracted_data['line_items'].extend(image_data['line_items'])
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            invoice = ManualInvoice.objects.create(
                user=request.user,
                uploaded_file=uploaded_file,
                parsed_data=extracted_data,
                status='completed'
            )

            return Response({
                "id": invoice.id,
                "key_fields": extracted_data['key_fields'],
                "line_items": extracted_data['line_items']
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
