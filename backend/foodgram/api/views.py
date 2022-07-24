from urllib import request, response
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from recipes.models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    #lookup_field = 'slug'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (AdminOrReadOnly,)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('name',)


class IngredientViewSet(viewsets.ModelViewSet):
    #lookup_field = 'slug'
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = (AdminOrReadOnly,)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    #lookup_field = 'slug'
    queryset = Recipe.objects.all()
    #serializer_class = RecipeSerializer
    # permission_classes = (AdminOrReadOnly,)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

