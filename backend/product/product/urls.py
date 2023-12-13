from django.urls import path
from .views import ProductViewSet, TesteView, OpenProductViewSet
urlpatterns=[
    path("", ProductViewSet.as_view({
        "post": "save",

    })),
    
     path("all", OpenProductViewSet.as_view({
        "get": "retrieveList",

    })),

    path("<int:id>", OpenProductViewSet.as_view({
        "get": "retrieve"
    })),

    
    path("testeAuth", TesteView.as_view())
]