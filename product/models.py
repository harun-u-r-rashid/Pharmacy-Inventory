from django.db import models
from user.models import User


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(unique=True, max_length=105, blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Purchase(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    purchase_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"{self.user}-----{self.product.name} ----- {self.quantity}"


class Sell(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    sell_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"{self.user}-----{self.product.name} ----- {self.quantity}"
