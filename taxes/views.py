from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TaxRate
from .serializers import TaxRateSerializer
from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated

class TaxRateCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = TaxRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaxRateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = TaxRate.objects.filter(is_active=True)
        serializer = TaxRateSerializer(queryset, many=True)
        return Response(serializer.data)
