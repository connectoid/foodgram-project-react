from urllib import request, response
from django.db import IntegrityError
from django.shortcuts import render

from django.http import Http404, HttpResponse
from rest_framework import viewsets, status, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import filters
from django.db.models import Sum
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)

from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, IngredientToRecipe
from .serializers import TagSerializer, IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer, RecipeFavoriteSerializer #, ShoppingCartSerializer
from .permissions import OwnerOrReadOnly, ReadOnly
from .filters import RecipeFilter, IngredientSearchFilter
from .paginations import RecipePageNumberPagination, ShoppingCartPageNumberPagination

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('name',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (SearchFilter, )
    filterset_class = IngredientSearchFilter
    search_fields = ('^name', )

class RecipeViewSet(viewsets.ModelViewSet):
    #lookup_field = 'slug'
    queryset = Recipe.objects.all()
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    #serializer_class = RecipeSerializer
    # permission_classes = (AdminOrReadOnly,)
    pagination_class = RecipePageNumberPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('name',)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    
    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def add_favorite(self, request, recipe):
        try:
            Favorite.objects.create(user=request.user, recipe=recipe)
        except IntegrityError:
            return Response(
                {'errors': 'already exists'},
                status=HTTP_400_BAD_REQUEST,
            )
        serializer = RecipeFavoriteSerializer(recipe)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def delete_favorite(self, request, recipe):
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if not favorite.exists():
            return Response(
                {'errors': 'dont exists'},
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


class ShoppingCartViewSet(GenericViewSet):
    NAME = 'ingredients__ingredient__name'
    MEASUREMENT_UNIT = 'ingredients__ingredient__measurement_unit'
    pagination_class = ShoppingCartPageNumberPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeFavoriteSerializer
    queryset = ShoppingCart.objects.all()
    http_method_names = ('get', 'post', 'delete',)

    def generate_shopping_cart_data(self, request):
        recipes = (
            request.user.shopping_cart.recipes.prefetch_related('ingredients')
        )
        return (
            recipes.order_by(self.NAME)
            .values(self.NAME, self.MEASUREMENT_UNIT)
            .annotate(total=Sum('ingredients__amount'))
        )

    def generate_ingredients_content(self, ingredients):
        content = ''
        for ingredient in ingredients:
            content += (
                f'{ingredient[self.NAME]}'
                f' ({ingredient[self.MEASUREMENT_UNIT]})'
                f' — {ingredient["total"]}\r\n'
            )
        return content

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        FILENAME = 'shopping_cart.txt'
        try:
            ingredients = self.generate_shopping_cart_data(request)
        except ShoppingCart.DoesNotExist:
            return Response(
                {'errors': 'список отсутствует'},
                status=HTTP_400_BAD_REQUEST
            )
        content = self.generate_ingredients_content(ingredients)
        response = HttpResponse(
            content, content_type='text/plain,charset=utf8'
        )
        response['Content-Disposition'] = f'attachment; filename={FILENAME}'
        return response

    def add_to_shopping_cart(self, request, recipe, shopping_cart):
        if shopping_cart.recipes.filter(pk__in=(recipe.pk,)).exists():
            return Response(
                {'errors': 'уже добавлен'},
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
                {'errors': 'рецепта нет'},
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
