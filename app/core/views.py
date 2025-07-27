
from rest_framework import viewsets
from .models import Client, CreditOffer, Moderator
from .serializers import ClientSerializer, CreditOfferSerializer, ModeratorSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CreditOfferViewSet(viewsets.ModelViewSet):
    queryset = CreditOffer.objects.all()
    serializer_class = CreditOfferSerializer

class ModeratorViewSet(viewsets.ModelViewSet):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer
