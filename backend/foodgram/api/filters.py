from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import (AllValuesMultipleFilter,
                                           BooleanFilter, CharFilter,
                                           FilterSet)

from recipes.models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        favorites = self.request.user.favorites.all()
        return queryset.filter(pk__in=favorites.values('id'))

    def get_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        try:
            recipes = (
                self.request.user.shopping_cart.recipes.all()
            )
        except ObjectDoesNotExist:
            return queryset
        return queryset.filter(pk__in=recipes.valuse('id'))


class IngredientSearchFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
