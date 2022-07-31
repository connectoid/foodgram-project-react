from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
                    TagViewSet)

router = routers.SimpleRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes', ShoppingCartViewSet, basename='shopping_cart')

urlpatterns = [
    path('', include(router.urls)),
]
