from rest_framework import request, response, views, viewsets, permissions, status
from rest_framework_api_key import permissions as apiKeyPermissions
from django.shortcuts import get_object_or_404
from .models import Cart
from .serializer import CartSerializer


class CartMixin(views.APIView):
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    

class OpenCartMixin(views.APIView):
    
    permission_classes = (permissions.AllowAny, )
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    

class OpenCartViewSet(OpenCartMixin, viewsets.ViewSet):
    
    def retrieveCart(self, request, *args, **kwargs):
        
        userId = kwargs.get("userId")
        
        if not userId:
            return response.Response({"err": "No ID provided"}, status.HTTP_400_BAD_REQUEST)

        
        cart = get_object_or_404(Cart, userId=userId)
        
        serializer = self.serializer_class(cart)
        
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class CartViewSet(CartMixin, viewsets.ViewSet):
    
    
    def save(self,request, *args, **kwargs):
        
        cartBody = {
            "userId": request.data["userId"],
            "products": request.data["products"]
        }
        
        serializer = self.serializer_class(data=cartBody)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response({"err": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
   
    def retrieveCart(self, request, *args, **kwargs):
        
        userId = kwargs.get("userId")
        
        if not userId:
            return response.Response({"err": "No ID provided"}, status.HTTP_400_BAD_REQUEST)

        
        cart = get_object_or_404(Cart, userId=userId)
        
        serializer = self.serializer_class(cart)
        
        return response.Response(serializer.data, status=status.HTTP_200_OK)