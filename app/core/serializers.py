from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class CreditOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditOffer
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class FeedbackConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackConfig
        fields = '__all__'

