from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from recipe.models import Ingredient, Recipe
from recipe.serializers import RecipeSerializer
import json


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_sample_recipe(name='Sample recipe', description='Sample description'):
    """Create a sample recipe"""
    return Recipe.objects.create(
        name=name,
        description=description
    )


def create_sample_ingredient(name='Sample ingredient'):
    """Create a sample ingredient"""
    return Ingredient.objects.create(name=name)


class RecipeApiTests(APITestCase):
    """Test recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_get_recipes(self):
        """Test that the list of recipes can be retrieved (GET)"""
        # Create a recipe and serialize it
        recipe = create_sample_recipe()
        serializer = RecipeSerializer(recipe)

        # Retrieve the list of recipes
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify the list returned is correct
        self.assertEqual(len(res.data), 1)
        self.assertIn(serializer.data, res.data)

    def test_create_recipe_no_ingredients(self):
        """"Test that we can create (POST) a recipe without ingredients"""
        # Create a recipe calling the API
        payload = {
            'name': 'New recipe',
            'description': 'This is a description',
            'ingredients': []
        }
        res = self.client.post(RECIPES_URL, json.dumps(payload),
                               content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Verify the recipe was created correctly
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(payload['name'], getattr(recipe, 'name'))
        self.assertEqual(payload['description'], getattr(recipe, 'description'))

    def test_create_recipe_with_ingredients(self):
        """"Test that we can create (POST) a recipe with ingredients"""
        # Create a recipe calling the API
        payload = {
            'name': 'Salad',
            'description': 'This is a description',
            'ingredients': [
                {'name': 'Tomato'},
                {'name': 'Cucumber'},
                {'name': 'Lettuce'}
            ]
        }
        res = self.client.post(RECIPES_URL, json.dumps(payload),
                               content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Verify the recipe was created correctly
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(payload['name'], getattr(recipe, 'name'))
        self.assertEqual(payload['description'], getattr(recipe, 'description'))
        # Verify the ingredients were created correctly
        self.assertEqual(len(recipe.ingredients.all()), 3)
        for ingredient in res.data['ingredients']:
            self.assertTrue(Ingredient.objects.filter(name=ingredient['name']).exists())

    def test_edit_recipe_partial_no_ingredients(self):
        """Test that we can partially edit (PATCH) a recipe, without altering ingredients"""
        # Create a recipe
        recipe = create_sample_recipe()
        recipe.ingredients.add(create_sample_ingredient())

        # Update the recipe calling the API
        payload = {'name': 'Cucumber salad'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Refresh the recipe object from DB
        recipe.refresh_from_db()

        # Verify the recipe's name was updated but it still has one ingredient
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(len(recipe.ingredients.all()), 1)

    def test_edit_recipe_partial_with_ingredients(self):
        """Test that we can partially edit (PATCH) a recipe, altering ingredients"""
        # Create a recipe
        recipe = create_sample_recipe()
        recipe.ingredients.add(create_sample_ingredient())

        # Update the recipe calling the API
        payload = {
            'name': 'Cucumber salad',
            'ingredients': [
                {'name': 'Onion'}
            ]
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Refresh the recipe object from DB
        recipe.refresh_from_db()

        # Verify the recipe's name and ingredients were updated
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(len(recipe.ingredients.all()), 1)
        self.assertTrue(Ingredient.objects.filter(
            name=res.data['ingredients'][0]['name']
        ).exists())

    def test_edit_recipe_full(self):
        """Test that we can fully edit (PUT) a recipe"""
        # Create a recipe with one ingredient
        recipe = create_sample_recipe()
        recipe.ingredients.add(create_sample_ingredient())

        # Update the recipe calling the API
        payload = {
            #'id': recipe.id, # why do I have to put the ID here if it is in the URL?
            'name': 'Cucumber salad',
            'description': 'Cut all the cucumbers first',
            'ingredients': []
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, json.dumps(payload),
                               content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Refresh the recipe object from DB
        recipe.refresh_from_db()

        # Verify the recipe was updated
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(len(recipe.ingredients.all()), 0)
