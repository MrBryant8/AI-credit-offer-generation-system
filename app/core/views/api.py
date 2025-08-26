from rest_framework import viewsets
from ..models import Client, CreditOffer, User, Chat, Loan, AgentConfig
from ..serializers import ClientSerializer, CreditOfferSerializer, UserSerializer, ChatSerializer, LoanSerializer, AgentConfigSerializer

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

class AgentConfigViewSet(viewsets.ModelViewSet):
    queryset = AgentConfig.objects.all()
    serializer_class = AgentConfigSerializer
