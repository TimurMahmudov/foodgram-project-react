from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Subscription
from recipes.models import Recipe

User = get_user_model()

INVALID_USERNAMES = ['me', 'admin', 'user', 'username']


class UserAfterRegisterSerializer(serializers.ModelSerializer):
    """Отображение после регистрации"""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class UserRegisterSerializer(serializers.ModelSerializer):
    """Регистрация пользователя"""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def to_representation(self, instance):
        serializer = UserAfterRegisterSerializer(instance)
        return serializer.data

    def validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError(
                'Пароль должен быть не менее 8 символов'
            )
        if data['username'] in INVALID_USERNAMES:
            raise serializers.ValidationError(
                'Логин не может быть одним из: {}, {}, {}, {}'.format(*INVALID_USERNAMES)
            )
        return data


class UserReadSerializer(serializers.ModelSerializer):
    """Просмотр пользователя"""
    is_subscribed = serializers.SerializerMethodField('get_subscribed')

    class Meta:
        model = User
        fields = ('email', 'id', 'first_name', 'last_name', 'username', 'is_subscribed')

    def get_subscribed(self, obj):
        return Subscription.objects.filter(
            subscriber=self.context['request'].user,
            author=obj
        ).exists()


class RecipeFromTheAuthor(serializers.ModelSerializer):
    """Список рецептов от данного автора"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AuthorOfRecipesSerializer(UserReadSerializer):
    """Авторы, на которых подписан пользователь"""
    recipes = RecipeFromTheAuthor(many=True, source='recipes')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'first_name', 'last_name',
                  'username', 'is_subscibed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки"""

    class Meta:
        model = Subscription
        fields = ('subscriber', 'author')

    def validate(self, data):
        user, author = data['subscriber'], data['author']
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        if Subscription.objects.filter(subscriber=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на данного автора!'
            )
        return data
