from rest_framework import serializers
from .models import StockSlot

class StockSlotSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StockSlot
        fields = "__all__"
        
    def create(validated_data):
        return StockSlot.objects.create(**validated_data)
    
   