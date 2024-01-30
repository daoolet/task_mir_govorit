from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.ProductsView.as_view(), name="products_view"),
    path("recipes/", views.RecipesView.as_view(), name="recipes_view"),

    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
]


