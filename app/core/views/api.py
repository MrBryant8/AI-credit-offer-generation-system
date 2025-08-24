from rest_framework import viewsets
from ..models import Client, CreditOffer, User, Chat, Loan
from ..serializers import ClientSerializer, CreditOfferSerializer, UserSerializer, ChatSerializer, LoanSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CreditOfferViewSet(viewsets.ModelViewSet):
    queryset = CreditOffer.objects.all()
    serializer_class = CreditOfferSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
