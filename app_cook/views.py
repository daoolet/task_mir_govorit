from django.shortcuts import render


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import Product, Recipe, RecipeProduct
from .serializers import ProductSerializer, RecipeSerializer
from . import utils


@api_view(["GET"])
def index(request):
    return Response("This is GET", status=status.HTTP_200_OK)


class ProductsView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = utils.get_all_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_418_IM_A_TEAPOT)
    
    # @extend_schema(request=ProductSerializer)
    def post(self, request):
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
    

class ProductsDetialView(APIView):
    def get(self, request, product_id):
        product = utils.get_object(Product, product_id)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        product = utils.get_object(Product, product_id)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({"detail": "Successful"}, status=status.HTTP_200_OK)


class RecipesView(APIView):
    serializer_class = RecipeSerializer
    
    def get(self, request):
        recipes = utils.get_all_recipes()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_418_IM_A_TEAPOT)

    # @extend_schema(request=RecipeSerializer)
    def post(self, request):
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
    

class RecipesDetailView(APIView):
    def get(self, request, recipe_id):
        recipe = utils.get_object(Recipe, recipe_id)
        if recipe is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, recipe_id):
        recipe = utils.get_object(Recipe, recipe_id)
        if recipe is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        recipe.delete()
        return Response({"detail": "Successful"}, status=status.HTTP_200_OK)
    
