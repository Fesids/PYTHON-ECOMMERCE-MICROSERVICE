from django.db import models

# Create your models here.
class StockSlot(models.Model):
    productId = models.IntegerField(null=False, unique=True)
    productName = models.CharField(max_length=244, null=False)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.productName} - {self.productId}"
    