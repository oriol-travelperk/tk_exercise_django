from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.models import Ingredient, Recipe
from recipe.serializers import RecipeSerializer


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


class RecipeApiTests(TestCase):
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

    def test_create_recipe(self):
        """"Test that we can create (POST) a recipe"""
        # Create a recipe calling the API
        payload = {
            'name': 'New recipe',
            'description': 'This is a description'
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Verify the recipe was created
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_edit_recipe_partial(self):
        """Test that we can partially edit (PATCH) a recipe"""
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

    def test_edit_recipe_full(self):
        """Test that we can fully edit (PUT) a recipe"""
        # Create a recipe
        recipe = create_sample_recipe()
        recipe.ingredients.add(create_sample_ingredient())

        # Create a new ingredient that we will add to the recipe
        new_ingredient = create_sample_ingredient(name='Cucumber')
        # Update the recipe calling the API
        payload = {
            'name': 'Cucumber salad',
            'ingredients': [new_ingredient.id]
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Refresh the recipe object from DB
        recipe.refresh_from_db()

        # Verify the recipe was updated, name and ingredients
        self.assertEqual(recipe.name, payload['name'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(len(ingredients), 1)
        self.assertIn(new_ingredient, ingredients)
