from django.db import models
from django.db.models import F
from django.shortcuts import get_object_or_404

from .models import Product, Recipe, RecipeProduct


def get_all_products():
    return Product.objects.all()

def get_all_recipes():
    return Recipe.objects.all()

def product_exists(name: str):
    return Product.objects.filter(name=name.lower()).exists()

def recipe_exists(name: str):
    return Recipe.objects.filter(name=name.lower()).exists()

def get_object(model: models.Model, pk: int):
    try:
        return get_object_or_404(model, pk=pk)
    except model.DoesNotExist:
        return None

def add_product_to_recipe(
        recipe_id,
        product_id,
        weight
):
    current_recipe = Recipe.objects.filter(id=recipe_id)
    new_product = Product.objects.filter(id=product_id)
    product_in_recipe = False

    if current_recipe.exists() and new_product.exists():
        products_of_recipe = current_recipe.products.all()

        for product in products_of_recipe:
            if product.id == new_product.id:
                RecipeProduct.objects.filter(product=new_product).update(weight=F("weight") + weight)
                product_in_recipe = True
                break
        
        if not product_in_recipe:
            current_recipe.product.add(new_product, through_defaults={"weight": weight})
        
        return "Success"
    return "Does not Exist"