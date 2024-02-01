from django.test import TestCase

from rest_framework.test import APITestCase


from .models import Product, Recipe, RecipeProduct

# Create your tests here.

class ModelsTest(TestCase):
    def test_create_product(self):
        p1 = Product.objects.create(name="milk")
        p2 = Product.objects.create(name="sugar")
        p3 = Product.objects.create(name="butter", amount_of_prep=10)

        self.assertEqual("milk", p1.name)
        self.assertEqual("sugar", p2.name)
        self.assertEqual("butter", p3.name)

        self.assertEqual(0, p1.amount_of_prep)
        self.assertEqual(10, p3.amount_of_prep)

        self.assertNotEqual("butter", p1.name)
    
    def test_create_recipe(self):
        r1 = Recipe.objects.create(name="syrniki")
        r2 = Recipe.objects.create(name="bliny")
        r3 = Recipe.objects.create(name="tort")

        all_recipes = Recipe.objects.all()
        query1 = Recipe.objects.filter(name="tort")
        query2 = Recipe.objects.filter(name="plov")

        self.assertIn(r1, all_recipes)
        self.assertIs(query1.exists(), True)
        self.assertFalse(query2.exists())

    def test_create_recipe_product(self):
        Product.objects.create(name="milk")
        Product.objects.create(name="sugar")
        Recipe.objects.create(name="bliny")

        p1 = Product.objects.get(name="milk")
        r1 = Recipe.objects.get(name="bliny")
        weight = 100

        RecipeProduct.objects.create(recipe_id=r1.id, product_id=p1.id, weight=100)

        rp1 = RecipeProduct.objects.get(id=1)
        print(rp1)
        # print(r1.products.all()) find all products of 1 recipe
        self.assertEqual(rp1.id, 1)
