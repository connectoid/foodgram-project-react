from django.urls import include, path
from rest_framework import routers

from .views import TagViewSet, IngredientViewSet, RecipeViewSet

router = routers.SimpleRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')



urlpatterns = [
    path('', include(router.urls)),
]