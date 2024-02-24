from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.ProductsView.as_view(), name="products_view"),
    path("products/<int:product_id>", views.ProductsDetialView.as_view(), name="products_detail_view"),

    path("recipes/", views.RecipesView.as_view(), name="recipes_view"),
    path("recipes/<int:recipe_id>", views.RecipesDetailView.as_view(), name="recipes_detail_view"),

    path("recipe_products/", views.RecipeProductsView.as_view(), name="recipe_products_view"),
    path("recipe_products/<str:recipe_name>/", views.RecipeProductsDetailView.as_view(), name="recipeproduct_detail_view"),
    path("recipe_products/delete/<str:recipe_name>/<str:product_name>/", views.delete_product_from_recipe, name="recipeproduct_delete"),

    path("add_product_to_recipe/<int:recipe_id>/<int:product_id>/<int:weight>/", views.add_product_to_recipe, name="task1"),
    path("cook_recipe/<int:recipe_id>/", views.cook_recipe, name="task2"),
    path("show_recipes_without_product/<int:product_id>/", views.show_recipes_without_product, name="task3"),

    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
]


