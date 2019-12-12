from rest_framework import serializers
from recipe.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        # Extract the ingredients data
        ingredients_data = validated_data.pop('ingredients')
        # Create the recipe object
        recipe = Recipe.objects.create(**validated_data)
        # Create the ingredient objects
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        # Update the recipe fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # Update ingredients field only if it exists
        if 'ingredients' in validated_data:
            # Delete all existing ingredients in this recipe
            instance.ingredients.all().delete()
            # Create the new ingredient objects
            ingredients_data = validated_data.pop('ingredients')
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(recipe=instance, **ingredient_data)

        instance.save()
        return instance
