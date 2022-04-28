from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import RegistrationSerializer, AssetsListSerializer, CoinSerializer
from rest_framework.authtoken.models import Token
import requests
from rest_framework import serializers

from .models import Favourite, User, Coin
from rest_framework import generics

import json


@api_view(['POST'])
def registeration_view(request, *args, **kwargs):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['message'] = "Created user successfully"
        data['full_name'] = account.full_name
        data['email'] = account.email
        token = Token.objects.get(user=account).key
        data['token'] = token
        return Response(data, status=200)
    data = serializer.errors
    return Response(data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assets_listView(request, *args, **kwargs):
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': '432DCB67-C825-4A65-B9A7-E5D8260C58A5'}
    response = requests.get(url, headers=headers)
    re = response.json()
    print("Hello world")
    data = []
    print('re : ' + str(re))
    index = 0
    for i in re:
        print('i : ' + str(i))
        dict = {
            "name": i["name"],
            "volume": i["volume_1hrs_usd"],
        }
        data.append(dict)  # ADDING DICTIONARY TO PARENT DICTIONARY
        index = index + 1
    print(type(re))
    serializer = AssetsListSerializer(data=data, many=True)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=200)
    return Response({}, status=404)



class AddFavouriteApiView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        if not 'username' in request.GET or not 'favourite' in request.GET:
            return Response(
                {'error': "invalid request, credentials  is incomplete,username or favourite missing"},
                status=405
            )

        username = request.GET['username']
        coin_to_add = request.GET['favourite']

        created, coin = Coin.objects.get_or_create(name__iexact=coin_to_add)
        user = User.objects.filter(username=username)

        if not user.exists():
            return Response(
                "The provided username is not a registered user",
                status=404
            )

        created, favourite_obj = Favourite.objects.get_or_create(user=user.first())
        if coin not in favourite_obj.coin.all():
            favourite_obj.coin.add(*[coin])
        json_response = {
            "message": "Added {} to favourite successfully".format(coin_to_add),
            "username": username,
            "coin-name": coin_to_add
        }

        return Response(
            json_response,
            status=200
        )


class ListFavouriteApiView(generics.ListAPIView):
    model = Favourite

    def get(self, request, *args, **kwargs):
        if not 'username' in request.GET:
            return Response(
                {'error': "invalid request, username is missing"},
                status=405
            )

        username = request.GET['username']
        favourites = self.model.objects.filter(
            user__username=username
        )
        if favourites.exists():
            serialized_favourite_coin_data = CoinSerializer(
                favourites.first().coin.all()
            ).data

            response = {}
            response['message'] = "welcome back {} ".format(username)
            response["subscribed_favourites"] = serialized_favourite_coin_data
            return Response(response, status=200)

        else:
            return Response(
                {
                    "message": "welcome back {} ".format(username),
                    "error": "You are yet to subscribe to any favourite"
                },
                status=200
            )
