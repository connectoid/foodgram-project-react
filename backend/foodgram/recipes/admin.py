from django.contrib import admin

from . import models
from users.models import User


class IngredientToRecipeInLine(admin.StackedInline):
    model = models.IngredientToRecipe
    extra = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'cook_time']
    inlines = [IngredientToRecipeInLine]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit']


@admin.register(models.IngredientToRecipe)
class IngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'unit', 'quantity']

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['login', 'name', 'fname', 'email', 'role']