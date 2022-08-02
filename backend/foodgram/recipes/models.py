from django.core import validators
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=150)
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
    slug = models.SlugField('Слаг', max_length=100)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=150)
    measurement_unit = models.CharField('Единица измерения', max_length=50)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', null=True, blank=True,
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientToRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    name = models.CharField('Название', max_length=150)
    image = models.ImageField('Изображение', upload_to='images/')
    text = models.TextField('Текст рецепта')
    cooking_time = models.PositiveIntegerField('Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pk',)

    def __str__(self):
        return self.name


class IngredientToRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name='ingredient_recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient_recipe',
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиентов в рецепте'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique ingredient recipe',
            ),
        )

    def __str__(self):
        return (f'Для рецепта {self.recipe} необходимо {self.amount}'
                f'{self.measurement_unit} {self.ingredient}')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
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
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipes = models.ManyToManyField(
        'recipes.Recipe',
        related_name='shopping_cart',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}'
