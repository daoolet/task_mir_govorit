from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.get_products, name="get_products"),
    path("recipes/", views.get_recipes, name="get_recipes"),

    path("products/add/", views.post_product, name="post_product"),
    path("recipes/add/", views.post_recipes, name="post_recipes"),

    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
]


