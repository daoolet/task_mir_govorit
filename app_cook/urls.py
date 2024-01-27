from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path("", views.api_index, name="index"),
    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
]


