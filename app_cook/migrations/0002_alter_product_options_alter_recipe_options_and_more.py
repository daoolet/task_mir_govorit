# Generated by Django 5.0.1 on 2024-02-24 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_cook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'Recipe', 'verbose_name_plural': 'Recipes'},
        ),
        migrations.AlterModelOptions(
            name='recipeproduct',
            options={'verbose_name': 'RecipeProduct', 'verbose_name_plural': 'RecipeProducts'},
        ),
    ]
