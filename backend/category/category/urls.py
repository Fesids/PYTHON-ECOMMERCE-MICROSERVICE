from django.urls import path

from .views import CategoryViewSet, CategoryOpenViewSet

urlpatterns = [
    path("", CategoryViewSet.as_view({
        "post": "save",
        

    })),

    path("<int:id>", CategoryOpenViewSet.as_view({
        "get": "retrieve",
    })),
    
     path("all", CategoryOpenViewSet.as_view({
        "get": "retrieveList"
    })),

    

]