from django.shortcuts import render
from rest_framework import viewsets, mixins
from recipe.models import Ingredient, Recipe
from recipe import serializers


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    """Ingredient viewset"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe viewset"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
