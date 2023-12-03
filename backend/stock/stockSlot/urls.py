from django.urls import path
from . import views

urlpatterns = [
    path("", views.StockSlotViewSet.as_view({
        "post": "save"
    })),
    
    path("<int:productId>", views.StockSlotViewSet.as_view({
        "get": "retrieveByProductId"
    })),
    
    path("check/<int:productId>", views.StockSlotViewSet.as_view({
        "get": "checkProductAvailable"
    }))
]