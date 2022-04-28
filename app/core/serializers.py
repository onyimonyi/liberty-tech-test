from builtins import len
from .models import User, Coin
from rest_framework import serializers
from django.conf import settings
ADD_FAV_COIN = settings.ADD_FAV_COIN


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=224, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password')


class AssetsListSerializer(serializers.Serializer):
    name = serializers.CharField()
    volume = serializers.CharField()


    def get_name(self, obj):
        return obj.name

    def get_volume(self, obj):
        return obj.volume


class AddFavCoinSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ADD_FAV_COIN:
            raise serializers.ValidationError("this is not a valid action to add coin")
        return value

class CoinSerializer(serializers.ModelSerializer) :

    class Meta() :
        model = Coin
        fields = ['name']
