from django.test import TestCase
from recipe.models import Ingredient, Recipe


class ModelTests(TestCase):

    def test_ingredient_str(self):
        """Test the ingredient string representation"""

        # Create a sample ingredient
        ingredient = Ingredient.objects.create(
            name='Sample ingredient'
        )

        # Verify the str representation is correct
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""

        # Create a sample recipe
        recipe = Recipe.objects.create(
            name='Sample recipe',
            description='Sample description'
        )

        # Verify the str representation is correct
        self.assertEqual(str(recipe), recipe.name)
