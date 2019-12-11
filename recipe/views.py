from django.shortcuts import render
from rest_framework import viewsets
from recipe.models import Ingredient, Recipe
from recipe import serializers


class IngredientViewSet(viewsets.ModelViewSet):
    """Ingredient viewset"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe viewset"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        """Return appropiate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class
