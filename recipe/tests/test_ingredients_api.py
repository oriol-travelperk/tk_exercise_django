from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class IngredientApiTests(TestCase):
    """Test ingredient API access"""

    def setUp(self):
        self.client = APIClient()

    def test_get_ingredients(self):
        """Test that the list of ingredients can be retrieved"""
        # Create a recipe & ingredient and serialize it
        recipe = Recipe.objects.create(name='Any recipe')
        ingredient = Ingredient.objects.create(recipe=recipe, name='Any ingredient')
        serializer = IngredientSerializer(ingredient)
        # Retrieve the list of ingredients
        res = self.client.get(INGREDIENTS_URL)

        # Verify the list returned is correct
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertIn(serializer.data, res.data)
