from django.db import models
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