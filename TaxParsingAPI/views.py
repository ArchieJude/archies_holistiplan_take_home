from rest_framework import viewsets
from TaxParsingAPI.models import TaxForm
from TaxParsingAPI.serializers import TaxFormSerializer
from rest_framework.permissions import IsAuthenticated

class TaxFormViewSet(viewsets.ModelViewSet):
    queryset = TaxForm.objects.all()
    serializer_class = TaxFormSerializer
    permission_classes = [IsAuthenticated]
