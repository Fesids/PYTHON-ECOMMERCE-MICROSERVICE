import json
from django.shortcuts import render
from rest_framework import response, status, views, viewsets, request, permissions
from django.shortcuts import get_object_or_404
from .models import StockSlot
from .serializers import StockSlotSerializer
# Create your views here.

class StockSlotMixin(views.APIView):
    queryset = StockSlot.objects.all()
    serializer_class = StockSlotSerializer
    
    
class StockSlotViewSet(StockSlotMixin, viewsets.ViewSet):
    
    
    def save(self, request, *args, **kwargs):
        
        sltBody = {
            "productId": request.data["productId"],
            "productName": request.data["productName"],
            "quantity": request.data["quantity"]
        }
        
        serializer = self.serializer_class.create(validated_data=sltBody)
        
        return response.Response({"success": True}, status=status.HTTP_201_CREATED)
    
    def checkProductAvailable(self, request, *args, **kwargs):
        
        productId = kwargs.get("productId")
        
        if not productId:
            return response.Response({"err": "No product ID provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        stock = StockSlot.objects.get(productId=productId)
        
        if not stock:
            return response.Response({"err": False}, status=status.HTTP_404_NOT_FOUND)
        
        return response.Response({"available": True}, status=status.HTTP_200_OK)
    
    def retrieveByProductId(self, request, *args, **kwargs):
        
        productId = kwargs.get("productId")
        
        if not productId:
            return response.Response({"err": "No product ID provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        stock = StockSlot.objects.get(productId=productId)
        
        serializer = self.serializer_class(stock)
        
        return response.Response(serializer.data, status=status.HTTP_200_OK)
        