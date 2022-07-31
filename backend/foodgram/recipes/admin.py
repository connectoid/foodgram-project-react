from django.contrib import admin

from users.models import Subscribe, User
from . import models
from .forms import TagForm


class IngredientToRecipeInLine(admin.StackedInline):
    model = models.IngredientToRecipe
    extra = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'cooking_time']
    inlines = [IngredientToRecipeInLine]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    form = TagForm


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']


@admin.register(models.IngredientToRecipe)
class IngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'amount']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'password',
        'first_name',
        'last_name',
        'email',
        'is_subscribed'
    ]


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']
