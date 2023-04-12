from django.contrib.auth import get_user_model, hashers
from recipes.models import Recipe
from rest_framework import serializers
from users.models import Subscription

User = get_user_model()

INVALID_USERNAMES = ['me', 'admin', 'user', 'username']
VALID_TEXT = 'Логин не может быть одним из: {}, {}, {}, {}'


class UserAfterRegisterSerializer(serializers.ModelSerializer):
    """
    Отображение после регистрации
    """

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Регистрация пользователя
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

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
                VALID_TEXT.format(*INVALID_USERNAMES)
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Введённый Email уже занят!'
            )
        return data

    def create(self, validated_data):
        data = validated_data
        data['password'] = hashers.make_password(data.get('password'))
        user = User.objects.create(**data)
        user.save()
        return user


class UserReadSerializer(serializers.ModelSerializer):
    """
    Просмотр пользователя
    """
    is_subscribed = serializers.SerializerMethodField('get_subscribed')

    class Meta:
        model = User
        fields = ('email', 'id', 'first_name',
                  'last_name', 'username', 'is_subscribed')

    def get_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=self.context['request'].user,
            author=obj
        ).exists()


class RecipeFromTheAuthor(serializers.ModelSerializer):
    """
    Список рецептов от данного автора
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AuthorOfRecipesSerializer(UserReadSerializer):
    """
    Авторы, на которых подписан пользователь
    """
    recipes = RecipeFromTheAuthor(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'first_name', 'last_name',
                  'username', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания подписки
    """

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def validate(self, data):
        user, author = data['user'], data['author']
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        if Subscription.objects.filter(user=user,
                                       author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на данного автора!'
            )
        return data
