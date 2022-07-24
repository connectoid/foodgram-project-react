from venv import create
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Tag, Ingredient, Recipe, IngredientToRecipe
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(read_only=True, source='ingredient.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientToRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientToRecipeSerializer(read_only=True, many=True, source='ingredient_recipe')
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = 'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart'


class RecipeWriteSerializer(serializers.ModelSerializer):
    #tags = TagSerializer(many=True)

    ingredients = IngredientToRecipeSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = 'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time'

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientToRecipe.objects.get_or_create(
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount'],
                recipe=recipe
            )
        return recipe
    
    
    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientToRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            IngredientToRecipe.objects.get_or_create(
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount'],
                recipe=instance
            )
        instance.tags.set(tags)
        return super().update(instance, validated_data)


    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance, context=self.context)
        return serializer.data

