from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    amount_of_prep = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural  = "Products"

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through="RecipeProduct")

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural  = "Recipes"

    def __str__(self):
        return self.name

class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()

    class Meta:
        verbose_name = "RecipeProduct"
        verbose_name_plural  = "RecipeProducts"
    
    def __str__(self):
        return f"This is {self.recipe} with {self.product} - {self.weight}"