from django.contrib import admin

from .models import Product, Recipe, RecipeProduct

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "amount_of_prep")

@admin.register(RecipeProduct)
class RecipeProductAdmin(admin.ModelAdmin):
    list_display = ("recipe", "product", "weight")
    list_filter = ("recipe", "product")


admin.site.register(Recipe)