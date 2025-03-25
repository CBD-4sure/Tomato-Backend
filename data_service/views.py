

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MenuDataTable, RestdataTable
from .serializers import MenuDataSerializer, ResDataSerializer


# Create your views here.
class ResDataApi(APIView):
    def get(self,request):
        
        res = RestdataTable.objects.all()
        seri = ResDataSerializer(res,many=True)

        return Response(seri.data)
    
    def post(self,request):
        url = "https://www.swiggy.com/dapi/restaurants/list/v5?lat=18.5204303&lng=73.8567437&page_type=DESKTOP_WEB_LISTING"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        data1 = response.json()
        cards = data1["data"]["cards"]
        for card in cards:
            if card["card"]["card"].get("id",False) == "restaurant_grid_listing_v2":
                resCards = card["card"]["card"]["gridElements"]["infoWithStyle"]["restaurants"]
        for res in resCards:
            resid = int(res["info"]["id"])
            if not RestdataTable.objects.filter(res_id=resid).first():
                serializer = ResDataSerializer(data={"data":res,"res_id":resid})
                if serializer.is_valid():
                    serializer.save()
        return Response(resCards[0])

class MenuDataApi(APIView):
    def get(self,request,resId):
        res = RestdataTable.objects.filter(res_id=resId)
        seriRes = ResDataSerializer(res,many=True)
        if not MenuDataTable.objects.filter(resId=resId).exists():
            response = requests.get("http://127.0.0.1:8000/data/u/"+str(resId))
        cards = MenuDataTable.objects.filter(resId=resId)
        seri = MenuDataSerializer(cards,many=True)
        return Response({"menudata":seri.data,"resData":seriRes.data})
    
        
class MenuUpdateApi(APIView):

    def get(self,request,resId):
        MENU_API = "https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.5204303&lng=73.8567437&restaurantId="

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        response = requests.get(MENU_API+str(resId), headers=headers)
        data = response.json()
        categories = data["data"]["cards"][4]["groupedCard"]["cardGroupMap"]["REGULAR"]["cards"]
        cards = []
        for c in categories:
            if c["card"]["card"]["@type"] == "type.googleapis.com/swiggy.presentation.food.v2.ItemCategory":
                cards.append(c)
        for c in cards:
            title = c["card"]["card"]["title"]
            if not MenuDataTable.objects.filter(resId=int(resId),title=title).exists():
                serialize = MenuDataSerializer(data={"data":c,"resId":int(resId),"title":title})
                if serialize.is_valid():
                    serialize.save()
        return Response(cards)