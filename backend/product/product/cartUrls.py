from django.urls import path
from .cartViews import CartViewSet, OpenCartViewSet

urlpatterns = [
    path("", CartViewSet.as_view({
        "post": "save",
    })),
    
    
    path("<int:userId>", OpenCartViewSet.as_view({
        "get": "retrieveCart"
    })),
    
]