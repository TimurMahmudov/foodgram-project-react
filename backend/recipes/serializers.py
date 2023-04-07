import base64

import webcolors
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import UserReadSerializer

from .models import (FavoriteRecipe, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)

User = get_user_model()

EXEC_UPDATE = "instance.{} = validated_data.get(field, instance.{})"


class Hex2NameColor(serializers.Field):
    """Сериализатор отображения цвета."""
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    """Форматирование изображения в строковый формат."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тегов."""
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра продуктов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов при создании рецепта."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов при просмотре рецепта."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Просмотр рецептов."""
    author = UserReadSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientInRecipeReadSerializer(many=True,
                                                   source='recipe_ingredient')
    is_favorited = serializers.SerializerMethodField('get_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField('get_shopping')
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()

    def get_shopping(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Создание рецепта."""
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    ingredients = IngredientInRecipeCreateSerializer(many=True)
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time',
                  'image', 'tags', 'ingredients')

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance, context=self.context)
        return serializer.data

    def create(self, validated_data):
        print(self.initial_data)
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)
        new_recipe.tags.set(tags)
        for ingredient_data in ingredients_data:
            IngredientInRecipe.objects.create(
                ingredient=ingredient_data['id'],
                recipe=new_recipe,
                amount=ingredient_data['amount']
            )
        new_recipe.save()
        return new_recipe

    def update(self, instance: Recipe, validated_data):
        ingredients = IngredientInRecipe.objects.filter(recipe=instance)
        ingredients.delete()
        new_ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        fields = instance._meta.fields
        exclude = []
        for field in fields:
            field = field.name.split('.')[-1]
            if field in exclude:
                continue
            exec(EXEC_UPDATE.format(field, field))
        instance.tags.set(tags)
        for ingredient_data in new_ingredients:
            IngredientInRecipe.objects.create(
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount'],
                recipe=instance
            )
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор Избранного"""

    class Meta:
        model = FavoriteRecipe
        fields = '__all__'

    def validate(self, data):
        recipe = data['recipe']
        user = self.context['request'].user
        if FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError(
                'Данный рецепт уже имеется у вас в Избранном!'
            )
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок"""

    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def validate(self, data):
        recipe = data['recipe']
        user = self.context['request'].user
        if ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError(
                'Данный рецепт уже занесён в список покупок!'
            )
        return data
