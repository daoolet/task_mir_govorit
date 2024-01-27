from django.shortcuts import render, get_object_or_404


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Recipe, RecipeProduct
from .serializers import ProductSerializer, RecipeSerializer
from . import utils


@api_view(["GET"])
def index(request):
    return Response("This is GET", status=status.HTTP_200_OK)


@api_view(["GET"])
def get_products(request):
    products = utils.get_all_products()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_418_IM_A_TEAPOT)


@api_view(["GET"])
def get_recipes(request):
    recipes = utils.get_all_recipes()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data, status=status.HTTP_418_IM_A_TEAPOT)


@api_view(["POST"])
def post_product(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        product_name = serializer.validated_data["name"]

        if utils.product_exists(name=product_name):
            return Response({"detail": "Already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            product = serializer.save()
            return Response({
                "detail": "Successful",
                "product_id": product.id,
                }, status=status.HTTP_200_OK)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def post_recipes(request):
    serializer = RecipeSerializer(data=request.data)

    if serializer.is_valid():
        recipe_name = serializer.validated_data["name"]

        if utils.recipe_exists(name=recipe_name):
            return Response({"detail": "Already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            recipe = serializer.save()
            return Response({
                "detail": "Successful",
                "recipe_id": recipe.id,
                }, status=status.HTTP_200_OK)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


