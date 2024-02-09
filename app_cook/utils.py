from django.db import models
from django.shortcuts import get_object_or_404

from .models import Product, Recipe, RecipeProduct


def get_all_records(model: models.Model):
    return model.objects.all()

def record_exists(model: models.Model, name: str):
    return model.objects.filter(name=name.lower()).exists()

def get_object(model: models.Model, pk: int):
    try:
        return get_object_or_404(model, pk=pk)
    except model.DoesNotExist:
        return None