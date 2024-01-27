from django.contrib import admin

from .models import Product, Recipe

# Register your models here.


admin.site.register(Product)
admin.site.register(Recipe)