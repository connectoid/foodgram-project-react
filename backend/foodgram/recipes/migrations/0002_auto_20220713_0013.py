# Generated by Django 2.2.16 on 2022-07-12 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientToRecipe', to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(to='recipes.Tag'),
        ),
        migrations.AddField(
            model_name='ingredienttorecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete='cascade', related_name='ingredient_recipe', to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='ingredienttorecipe',
            name='recipe',
            field=models.ForeignKey(on_delete='cascade', related_name='ingredient_recipe', to='recipes.Recipe'),
        ),
    ]
