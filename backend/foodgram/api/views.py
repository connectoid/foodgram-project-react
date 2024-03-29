from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import GenericViewSet

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .filters import IngredientSearchFilter, RecipeFilter
from .paginations import (RecipePageNumberPagination,
                          ShoppingCartPageNumberPagination)
from .permissions import OwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeFavoriteSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientSearchFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipePageNumberPagination
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_favorite(self, request, recipe):
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if favorite.exists():
            return Response(
                {'errors': 'Этот рецепт уже добавлен в избранные'},
                status=HTTP_400_BAD_REQUEST,
            )
        Favorite.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeFavoriteSerializer(recipe)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def delete_favorite(self, request, recipe):
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if not favorite.exists():
            return Response(
                {'errors': 'Этот рецепт не находится в избранных'},
                status=HTTP_400_BAD_REQUEST,
            )
        favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=('post', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            return self.add_favorite(request, recipe)
        return self.delete_favorite(request, recipe)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        INGREDIENT = 'ingredients__name'
        UNIT = 'ingredients__measurement_unit'
        FILENAME = 'shopping_cart.txt'
        recipes = (
            request.user.shopping_cart.recipes.prefetch_related('ingredients')
            )
        ingredients = recipes.values(INGREDIENT, UNIT).annotate(
            total=Sum('ingredients__ingredient_recipe__amount'))
        content = ''
        for ingredient in ingredients:
            content += (
                f'{ingredient[INGREDIENT]}'
                f' ({ingredient[UNIT]})'
                f' — {ingredient["total"]}\r\n'
                )
        response = HttpResponse(
            content, content_type='text/plain,charset=utf8'
        )
        response['Content-Disposition'] = f'attachment; filename={FILENAME}'
        return response


class ShoppingCartViewSet(GenericViewSet):
    pagination_class = ShoppingCartPageNumberPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeFavoriteSerializer
    queryset = ShoppingCart.objects.all()
    http_method_names = ('post', 'delete',)

    def add_to_shopping_cart(self, request, recipe, shopping_cart):
        if shopping_cart.recipes.filter(pk__in=(recipe.pk,)).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен в корзину'},
                status=HTTP_400_BAD_REQUEST,
            )
        shopping_cart.recipes.add(recipe)
        serializer = self.get_serializer(recipe)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def remove_from_shopping_cart(self, request, recipe, shopping_cart):
        if not shopping_cart.recipes.filter(pk__in=(recipe.pk,)).exists():
            return Response(
                {'errors': 'Рецепта в корзине нет'},
                status=HTTP_400_BAD_REQUEST,
            )
        shopping_cart.recipes.remove(recipe)
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    @action(methods=('post', 'delete',), detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart = (
            ShoppingCart.objects.get_or_create(user=request.user)[0]
        )
        if request.method == 'POST':
            return self.add_to_shopping_cart(request, recipe, shopping_cart)
        return self.remove_from_shopping_cart(request, recipe, shopping_cart)
