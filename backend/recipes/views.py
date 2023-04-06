from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Exists, OuterRef
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from users.serializers import RecipeFromTheAuthor

from .filters import RecipeFilter
from .models import (FavoriteRecipe, Ingredient, IngredientInRecipe,
                     Recipe, ShoppingCart, Tag)
from .permissions import AccessUpdateAndDelete
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeReadSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .shopping_cart import create_shopping_cart

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
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов"""
    serializer_class = RecipeReadSerializer
    queryset = Recipe.objects.all()
    permission_classes = (AccessUpdateAndDelete, )
    filter_backends = (DjangoFilterBackend, )
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return RecipeCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = Recipe.objects.select_related(
           'author'
        ).prefetch_related(
            'ingredients',
            'tags'
        )
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(
                    FavoriteRecipe.objects.filter(
                        user=user,
                        recipe=OuterRef('pk')
                    )
                ),
                is_in_shopping_cart=Exists(
                    ShoppingCart.objects.filter(
                        user=user,
                        recipe=OuterRef('pk')
                    )
                )
            )
        return queryset

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)

    # Добавление/удаление из Избранного
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_serializer = RecipeFromTheAuthor(recipe,
                                                context={'request': request})
        if request.method == 'POST':
            data = {'recipe': pk, 'user': user.id}
            serializer = FavoriteSerializer(data=data,
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
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_serializer = RecipeFromTheAuthor(recipe,
                                                context={'request': request})
        if request.method == 'POST':
            data = {'recipe': pk, 'user': user.id}
            serializer = ShoppingCartSerializer(data=data,
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

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        )
        shopping_list = create_shopping_cart(ingredients)
        file_name = "shopping_list.txt"
        response = HttpResponse(shopping_list, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; {file_name}"
        return response
