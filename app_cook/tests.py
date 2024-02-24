from django.test import TestCase
from django.db.models import F

from rest_framework.test import APITestCase


from .models import Product, Recipe, RecipeProduct

# Create your tests here.

class ModelsTest(TestCase):
    def setUp(self):
        Product.objects.create(name="milk")
        Product.objects.create(name="sugar")
        Product.objects.create(name="butter", amount_of_prep=10)

        Recipe.objects.create(name="syrniki")
        Recipe.objects.create(name="bliny")
        Recipe.objects.create(name="tort")

    def test_create_product(self):
        p1 = Product.objects.get(name="milk")
        p2 = Product.objects.get(name="sugar")
        p3 = Product.objects.get(name="butter")

        self.assertEqual("milk", p1.name)
        self.assertEqual("sugar", p2.name)
        self.assertEqual("butter", p3.name)

        self.assertEqual(0, p1.amount_of_prep)
        self.assertEqual(10, p3.amount_of_prep)

        self.assertNotEqual("butter", p1.name)
    
    def test_create_recipe(self):
        r1 = Recipe.objects.get(name="syrniki")
        r2 = Recipe.objects.get(name="bliny")
        r3 = Recipe.objects.get(name="tort")

        all_recipes = Recipe.objects.all()
        query1 = Recipe.objects.filter(name="tort")
        query2 = Recipe.objects.filter(name="plov")

        self.assertIn(r1, all_recipes)
        self.assertIs(query1.exists(), True)
        self.assertFalse(query2.exists())

    def test_create_recipe_product(self):
        p1 = Product.objects.get(name="milk")
        p2 = Product.objects.get(name="sugar")
        r1 = Recipe.objects.get(name="bliny")
        weight = 100

        RecipeProduct.objects.create(recipe_id=r1.id, product_id=p1.id, weight=weight)
        RecipeProduct.objects.create(recipe_id=r1.id, product_id=p2.id, weight=weight+50)

        rp1 = RecipeProduct.objects.get(id=1)
        rp2 = RecipeProduct.objects.get(id=2)
        all_products = rp1.recipe.products.all()

        # find all products of recipe
        # print(rp1.recipe.products.all()) 

        self.assertEqual(rp1.id, 1)
        self.assertEqual(rp2.id, 2)
        self.assertEqual([*all_products], [p1, p2])


class RecipeProductTest(TestCase):
    def setUp(self):
        Product.objects.create(name="milk")
        Product.objects.create(name="sugar")
        Product.objects.create(name="butter")

        Recipe.objects.create(name="syrniki")
        Recipe.objects.create(name="bliny")
        Recipe.objects.create(name="tort")

        p1 = Product.objects.get(name="milk")
        p2 = Product.objects.get(name="sugar")
        r1 = Recipe.objects.get(name="bliny")
        WEIGHT = 100

        RecipeProduct.objects.create(recipe_id=r1.id, product_id=p1.id, weight=WEIGHT)
        RecipeProduct.objects.create(recipe_id=r1.id, product_id=p2.id, weight=WEIGHT+50)

    def test_product_in_recipe(self):
        """
        Test case: if product already exists in the recipe, product's weight should be changed
        """
        new_product = Product.objects.get(name="milk")
        new_weight = 300
        rp1 = RecipeProduct.objects.get(id=1)
        rp2 = RecipeProduct.objects.get(id=2)
        all_products = rp1.recipe.products.all() # milk, sugar
        p1, p2 = all_products

        # print(rp1.weight)
        # print(rp2.weight)

        for product in all_products:
            if new_product.id == product.id:
                recipe_with_product = RecipeProduct.objects.get(product_id=product.id)
                recipe_with_product_weigth = recipe_with_product.weight
                print(product.id, recipe_with_product)

        object, created = RecipeProduct.objects.get_or_create(
            recipe_id=rp2.id,
            product_id=new_product.id,
            defaults={
                "weight": new_weight,
            }
        )
        if not created:
            object.weight += new_weight
            object.save()

        print(rp2, object)


class CookRecipeTest(TestCase):
    def setUp(self):
        Product.objects.create(name="milk")
        Product.objects.create(name="sugar")
        Product.objects.create(name="butter")

        Recipe.objects.create(name="syrniki")
        Recipe.objects.create(name="bliny")
        Recipe.objects.create(name="tort")

        p1 = Product.objects.get(name="milk")
        p2 = Product.objects.get(name="sugar")
        r1 = Recipe.objects.get(name="bliny")

        WEIGHT = 100

        # bliny - milk, sugar
        RecipeProduct.objects.create(recipe_id=r1.id, product_id=p1.id, weight=WEIGHT)
        RecipeProduct.objects.create(recipe_id=r1.id, product_id=p2.id, weight=WEIGHT+50)
    
    def test_task2(self):
        recipe_instance = Recipe.objects.get(id=2)
        self.assertEqual(recipe_instance.name, "bliny")

        rp = RecipeProduct.objects.filter(recipe_id=recipe_instance.id).last()
        print("*****TASK2*****")
        all_products = rp.recipe.products.all()
        for i in all_products:
            print(f"before {i} : {Product.objects.get(name=i).amount_of_prep}")
            print(f"after {i} : {Product.objects.filter(name=i).update(amount_of_prep=F("amount_of_prep") + 1)}")


