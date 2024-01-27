from rest_framework import serializers

from .models import Product, Recipe, RecipeProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "amount_of_prep"]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["name"]