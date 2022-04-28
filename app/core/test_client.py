import requests

url = "http://127.0.0.1:8000/api/auth/"

ctx ={
    'password' : "Kyletech99",
    'username' : 'tethub_5'
}
json = requests.post(url,json=ctx)
print(json.json())



















from rest_framework import serializers
from rest_framework.response import Response



class CoinSerializer(serializers.ModelSerializer) :

    class Meta() :
        model = Coin
        fields = ['name'] 


class AddFavouriteApiView(serializers.GenericAPIView) :
    
    def get(self,request,*args,**kwargs) :
        if not 'username' in request.GET or not 'favourite' in request.GET :
            return Response(
                {'error' : "invalid request, credentials  is incomplete,username or favourite missing"},
                status = 405
            )

        username = request.GET['username']
        coin_to_add = request.GET['favourite']

        created,coin = Coin.objects.get_or_create(name__iexact = coin_to_add)
        user = settings.AUTH_USER_MODEL.objects.filter(username = username)
        
        if not user.exists() : 
            return Response(
                "The provided username is not a registered user",
                status = 404
            )

        created,favourite_obj = Favourite.objects.get_or_create(user = user.first())
        if coin not in favourite_obj.coin.all() :
            favourite_obj.coin.add(*[coin])
        json_response = {
            "message" : "Added {} to favourite successfully".format(coin_to_add),
            "username" : username,
            "coin-name" : coin_to_add
        }
        
        return Response(
            json_response,
            status = 200
        )




class ListFavouriteApiView(generics.GenericAPIView)   :
    model = Favourite

    def get(self,request,*args,**kwargs) :
        if not 'username' in request.GET :
            return Response(
                {'error' : "invalid request, username is missing"},
                status = 405
            )

        username = request.GET['username']
        favourites  = self.model.objects.filter(
            user__username = username
        ) 
        if favourites.exists() :
            serialized_favourite_coin_data = CoinSerializer(
                favourites.first().coin.all()
            ).data

            response = {}
            response['message'] = "welcome back {} ".format(username)
            response["subscribed_favourites"] = serialized_favourite_coin_data
            return Response(response,status = 200)

        else :
            return Response(
                {
                    "message" :  "welcome back {} ".format(username),
                    "error" : "You are yet to subscribe to any favourite"
                },
                status = 200
            )    





