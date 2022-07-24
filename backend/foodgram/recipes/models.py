from tkinter import CASCADE
#from django.contrib.auth.models import User
from users.models import User
from django.db import models
from django.db.models import UniqueConstraint
from django.core import validators


class Tag(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        default='#569914',
        validators=[
            validators.RegexValidator(
                regex=r'#[a-f\d]{6}',
                message='Укажите цвет в HEX кодировке.'
            )
        ])
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=150)
    measurement_unit = models.CharField(max_length=50)
    #amount = amount = models.PositiveIntegerField('amount')
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientToRecipe',
        related_name='recipes'
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/') # !!!! CHECK
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()
    is_in_shopping_cart = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class IngredientToRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredient_recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient_recipe', on_delete=models.CASCADE)
    #measurement_unit = models.CharField(max_length=50)
    amount = models.PositiveIntegerField('amount')
    #instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return (f'Для рецепта {self.recipe} необходимо {self.amount} {self.measurement_unit} '
                f'{self.ingredient}')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique shopping cart')
        ]
