from rest_framework import serializers
from .models import Client, CreditOffer, Moderator

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class CreditOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditOffer
        fields = '__all__'


class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = '__all__'