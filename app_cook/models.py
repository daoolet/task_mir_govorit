from django.db import models

# Create your models here.


class Products(models.Model):
    product_name = models.CharField(max_length=255)
    amount_of_prep = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name
    

class Dishes(models.Model):
    dish_name = models.CharField(max_length=255)

    def __str__(self):
        return self.dish_name
    

class Recipes(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="dish_product")
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE, related_name="dish_product")
    weight = models.IntegerField()

    class Meta:
        unique_together = ('product', 'dish')
    
    def __str__(self):
        return f"Dish: {self.dish.dish_name} contains: {self.product.product_name}"