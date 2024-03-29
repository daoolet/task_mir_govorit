from django.shortcuts import render
from django.db.models import F, Count, Q

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import Product, Recipe, RecipeProduct
from .serializers import ProductSerializer, RecipeSerializer, RecipeProductSerializer
from . import utils


@api_view(["GET"])
def index(request):
    return Response("This is GET", status=status.HTTP_200_OK)


class ProductsView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = utils.get_all_records(Product)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_418_IM_A_TEAPOT)
    
    # @extend_schema(request=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            product_name = serializer.validated_data["name"]

            if utils.record_exists(Product, name=product_name):
                return Response({"detail": "Already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                product = serializer.save()
                return Response({
                        "detail": "Successful",
                        "product_id": product.id,
                    }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductsDetialView(APIView):
    def get(self, request, product_id: int):
        product = utils.get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, product_id: int):
        product = utils.get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({"detail": "Successful"}, status=status.HTTP_200_OK)


class RecipesView(APIView):
    serializer_class = RecipeSerializer
    
    def get(self, request):
        recipes = utils.get_all_records(Recipe)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_418_IM_A_TEAPOT)

    # @extend_schema(request=RecipeSerializer)
    def post(self, request):
        serializer = RecipeSerializer(data=request.data)

        if serializer.is_valid():
            recipe_name = serializer.validated_data["name"]

            if utils.record_exists(Recipe, name=recipe_name):
                return Response({"detail": "Already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                recipe = serializer.save()
                return Response({
                    "detail": "Successful",
                    "recipe_id": recipe.id,
                    }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RecipesDetailView(APIView):
    def get(self, request, recipe_id: int):
        recipe = utils.get_object_or_404(Recipe, id=recipe_id)
        if recipe is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, recipe_id: int):
        recipe = utils.get_object_or_404(Recipe, id=recipe_id)
        if recipe is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        recipe.delete()
        return Response({"detail": "Successful"}, status=status.HTTP_200_OK)
    

class RecipeProductsView(APIView):
    serializer_class = RecipeProductSerializer

    def get(self, request):
        recipe_products = utils.get_all_records(RecipeProduct)
        serializer = RecipeProductSerializer(recipe_products, many=True)
        return Response(serializer.data, status=status.HTTP_418_IM_A_TEAPOT)
    

class RecipeProductsDetailView(APIView):
    def get(self, request, recipe_name: str):
        try:
            current_recipe = Recipe.objects.get(name=recipe_name)
            recipe_product = RecipeProduct.objects.filter(recipe_id=current_recipe.id)
            serializer = RecipeProductSerializer(recipe_product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_product_from_recipe(self, request, recipe_name: str, product_name: str):
    try:
        current_recipe = Recipe.objects.get(name=recipe_name)
        current_product = Product.objects.get(name=product_name)
        current_recipe_product = RecipeProduct.objects.get(recipe_id=current_recipe.id, product_id=current_product.id)
        current_recipe_product.delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_200_OK)
    except Recipe.DoesNotExist or Product.DoesNotExist or RecipeProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(["GET"])
def add_product_to_recipe(
        request,
        recipe_id: int,
        product_id: int,
        weight: int | float
):

    current_recipe = utils.get_object_or_404(Recipe, id=recipe_id)
    new_product = utils.get_object_or_404(Product, id=product_id)

    recipe_product, created = RecipeProduct.objects.get_or_create(
        recipe_id=current_recipe.id,
        product_id=new_product.id,
        defaults={
            "weight": weight,
        }
    )

    if not created:
        recipe_product.weight += weight
        recipe_product.save()


    serializer1 = ProductSerializer(new_product)
    serializer2 = RecipeSerializer(current_recipe)
    serializer3 = RecipeProductSerializer(recipe_product)

    # serializer_list = [serializer1.data, serializer2.data, serializer3.data]
    content = {
        "product": serializer1.data,
        "recipe": serializer2.data,
        "recipe_product": serializer3.data,
    }

    return Response(content, status=status.HTTP_200_OK)


@api_view(["GET"])
def cook_recipe(request, recipe_id: int):
    recipe = utils.get_object_or_404(Recipe, id=recipe_id)
    recipe_product = RecipeProduct.objects.filter(recipe_id=recipe.id)

    if not recipe_product.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    all_products = recipe_product.last().recipe.products.all()
    for product in all_products:
        Product.objects.filter(name=product).update(amount_of_prep=F("amount_of_prep") + 1)

    serializer1 = ProductSerializer(all_products, many=True)
    return Response(serializer1.data, status=status.HTTP_200_OK)


def show_recipes_without_product(request, product_id: int):
    try:
        current_product = Product.objects.get(id=product_id)
        recipe_product_ids = list(RecipeProduct.objects.values_list("recipe_id", flat=True).distinct())

        kucha = {Recipe.objects.get(id=id): RecipeProduct.objects.filter(recipe_id=id).last().recipe.products.all() for id in recipe_product_ids}

        recipes_without_product = []

        for rec, prod in kucha.items():
            if current_product not in prod:
                recipes_without_product.append(rec)

        recipes_low_weight = []
        LOW_WEIGHT = 10
        
        recipes_with_product = RecipeProduct.objects.filter(product_id=current_product.id)
        for item in recipes_with_product:
            if item.weight < LOW_WEIGHT:
                recipes_low_weight.append(item.recipe)

        content = {
            "recipes_without_product": recipes_without_product,
            "recipes_low_weight": recipes_low_weight,
            "current_product": current_product,
        }
        return render(request, "app_cook/index.html", content)
    
    except Product.DoesNotExist:
        content = {
            "message": "Product does not exist in Products list" 
        }
        return render(request, "app_cook/index.html", content)