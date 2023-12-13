import requests
from django.shortcuts import render
from .serializer import CategorySerializer
from .models import Category
from rest_framework.response import Response
from rest_framework import views, viewsets, status, permissions, decorators as rest_decorators, request, authentication
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


class CategoryMixin(views.APIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class OpenCategoryMixin(views.APIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryOpenViewSet(OpenCategoryMixin, viewsets.ViewSet):
    
    def retrieveList(self, request, *args, **kwargs):
        categories = self.queryset

        serializer = self.serializer_class(categories, many=True)

        return Response(serializer.data, status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        categoryId = kwargs.get("id")

        category = get_object_or_404(Category, id=categoryId)

        serializer = None

        if category:
            serializer = self.serializer_class(category)

            return Response(serializer.data, status.HTTP_200_OK)

        return Response({"err": f"category with id {categoryId} not found"}, status.HTTP_404_NOT_FOUND)



class CategoryViewSet(CategoryMixin, viewsets.ViewSet):

    def save(self, request, *args, **kwargs):

        newCategoryBody = {
            "name": request.data["name"]
        }

        serializer = self.serializer_class(data=newCategoryBody)

        if serializer.is_valid():

            serializer.save()

            return Response({"success": serializer.data}, status.HTTP_200_OK)

        return Response({"err": serializer.errors}, status.HTTP_400_BAD_REQUEST)





