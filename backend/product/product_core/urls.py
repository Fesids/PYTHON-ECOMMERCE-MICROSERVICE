
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/product/", include("product.urls")),
    path("api/v1/cart/", include("product.cartUrls"))
    
]
