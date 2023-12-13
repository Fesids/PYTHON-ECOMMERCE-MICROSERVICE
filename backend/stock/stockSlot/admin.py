from django.contrib import admin
from .models import StockSlot
# Register your models here.
@admin.register(StockSlot)
class StockSlotAdmin(admin.ModelAdmin):
    
    fields = ["productName", "productId"]
