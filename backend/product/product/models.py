from django.db import models

# Create your models here.


class Product(models.Model):

    name = models.CharField(max_length=244, blank=False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    product_image = models.ImageField(upload_to="uploads/product", blank=True, null=True, default=" ")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    
    userId = models.IntegerField(null=False, blank=False)
    products = models.ManyToManyField("Product", related_name="products", null=True)
    
    def __str__(self):
        return f"cart owner ID {self.userId}"

