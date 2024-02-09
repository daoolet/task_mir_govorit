from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.ProductsView.as_view(), name="products_view"),
    path("products/<int:product_id>", views.ProductsDetialView.as_view(), name="products_detail_view"),
    path("recipes/", views.RecipesView.as_view(), name="recipes_view"),
    path("recipes/<int:recipe_id>", views.RecipesDetailView.as_view(), name="recipes_detail_view"),
    path("recipe_products/", views.RecipeProductView.as_view(), name="recipe_products_view"),

    path("add_product_to_recipe/<int:recipe_id>/<int:product_id>/<int:weight>/", views.add_product_to_recipe, name="task1"),

    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
]


