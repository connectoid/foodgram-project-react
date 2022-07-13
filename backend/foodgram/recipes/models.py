from tkinter import CASCADE
#from django.contrib.auth.models import User
from users.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=150)
    color = models.PositiveIntegerField()
    slug = models.SlugField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    title = models.CharField(max_length=150)
    unit = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/') # !!!! CHECK
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientToRecipe',
        related_name='recipes'
    )
    tag = models.ManyToManyField(Tag)
    cook_time = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.title


class IngredientToRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredient_recipe', on_delete=CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient_recipe', on_delete=CASCADE)
    unit = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    #instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return (f'Для рецепта {self.recipe} необходимо {self.quantity} {self.unit} '
                f'{self.ingredient}')
                