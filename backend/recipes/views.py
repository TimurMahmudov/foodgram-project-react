from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import (FavoriteRecipe, Ingredient,
                     Recipe, ShoppingCart, Tag)
from .serializers import (FavoriteSerializer, ShoppingCartSerializer,
                          RecipeReadSerializer, RecipeCreateSerializer,
                          TagSerializer, IngredientSerializer)
from users.serializers import RecipeFromTheAuthor

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тегов. Только чтение"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингредиентов. Только чтение"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, )


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов"""
    serializer_class = RecipeReadSerializer
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend, )

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return RecipeCreateSerializer
        return super().get_serializer_class()

    # Добавление/удаление из Избранного
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def favorite(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=id)
        recipe_serializer = RecipeFromTheAuthor(recipe,
                                                context={'request': request})
        if request.method == 'POST':
            data = {'recipe': id, 'user': user.id}
            serializer = FavoriteSerializer(data,
                                            context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(recipe_serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        favorite = FavoriteRecipe.objects.filter(user=user, recipe=recipe)
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Добавление/удаление из списка покупок
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def shopping_cart(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=id)
        recipe_serializer = RecipeFromTheAuthor(recipe,
                                                context={'request': request})
        if request.method == 'POST':
            data = {'recipe': id, 'user': user.id}
            serializer = ShoppingCartSerializer(data,
                                                context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(recipe_serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_recipe = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if shopping_recipe.exists():
            shopping_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
