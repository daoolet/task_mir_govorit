from django.contrib import admin

from .models import Products, Dishes, Recipes

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ("product_name", "amount_of_prep")
    list_filter = ("product_name",)


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('dish', 'product', 'weight')
    list_filter = ('dish', 'product')
    search_fields = ('dish__dish_name', 'product__product_name')

admin.site.register(Products, ProductsAdmin)
admin.site.register(Dishes)
admin.site.register(Recipes, RecipesAdmin)