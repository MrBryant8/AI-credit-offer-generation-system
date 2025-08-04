from rest_framework import viewsets
from ..models import Client, CreditOffer, User, Chat, Message, Loan
from ..serializers import ClientSerializer, CreditOfferSerializer, UserSerializer, ChatSerializer, MessageSerializer, LoanSerializer
from ..views.general import deactivate_old_credit_offers

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CreditOfferViewSet(viewsets.ModelViewSet):
    deactivate_old_credit_offers()
    queryset = CreditOffer.objects.all()
    serializer_class = CreditOfferSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
