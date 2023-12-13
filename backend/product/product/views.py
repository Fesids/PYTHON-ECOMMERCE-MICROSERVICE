import json
import jwt
from django.shortcuts import render
from rest_framework import status, response, views, viewsets, permissions, decorators as rest_decorators, request, authentication
from rest_framework_api_key import permissions as apiKeyPermissions
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework_simplejwt.tokens import AccessToken

from .models import Product
from .serializer import ProductSerializer
from .customPermissions import IsExternal
# Create your views here.


class TesteView(views.APIView):
    permission_classes = [
        IsExternal
    ]
    def get(self, request):
        return response.Response("Teste")

class ProductMixin(views.APIView):
   
    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    
class OpenProductMixin(views.APIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class OpenProductViewSet(OpenProductMixin, viewsets.ViewSet):
    
    
    def retrieveList(self, request):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many=True)

        if not products:
            return response.Response({"err": "No product found"})

        return response.Response(serializer.data, status.HTTP_200_OK)


    def retrieve(self, request, *args,**kwargs):

        request_id = kwargs.get("id")

        if not request_id:
            return response.Response({"err": "No ID provided"}, status.HTTP_400_BAD_REQUEST)

        request = get_object_or_404(Product, id=request_id)

        serializer = self.serializer_class(request)

        return response.Response(serializer.data, status.HTTP_200_OK)



class ProductViewSet(ProductMixin,viewsets.ViewSet):


    def save(self, request, *args, **kwargs):
        newBodyProduct = {
            "name": request.data["name"],
            "description": request.data["description"],
            "product_image": request.data["product_image"],
            "price": request.data["price"],
            "category": request.data["category"]
        }

        serializer = self.serializer_class(data=newBodyProduct)

        if serializer.is_valid():

            serializer.save()

            return response.Response({"success": serializer.data}, status.HTTP_201_CREATED)

        return response.Response({"err": serializer.errors}, status.HTTP_400_BAD_REQUEST)

