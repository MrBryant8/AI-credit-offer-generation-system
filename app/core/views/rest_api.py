from rest_framework import viewsets
from ..models import *
from ..serializers import *


"""
    REST Interface for the Models in the context if the Project.
"""
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

class AgentFeedbackViewSet(viewsets.ModelViewSet):
    queryset = AgentFeedback.objects.all()
    serializer_class = AgentFeedbackSerializer
