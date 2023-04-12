from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from recipes.models import (FavoriteRecipe, Ingredient, IngredientInRecipe,
                            Recipe, ShoppingCart, Tag)
from .filters import RecipeFilter
from .mixins import CreateDestroyObjView
from .permissions import AccessUpdateAndDelete
from .recipes_serializers import (FavoriteSerializer, IngredientSerializer,
                                  RecipeCreateSerializer, RecipeReadSerializer,
                                  ShoppingCartSerializer, TagSerializer)
from .shopping_cart import create_shopping_cart
from .users_serializers import RecipeFromTheAuthor

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет тегов. Только чтение
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет ингредиентов. Только чтение
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет рецептов
    """
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

    """
    Скачивание файла .TXT списка покупок
    """
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
        response = FileResponse(shopping_list, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; {file_name}"
        return response


class ShoppingCartViewSet(CreateDestroyObjView):
    """
    Добавление/удаление рецепта из списка покупок
    """
    serializer_class = ShoppingCartSerializer
    model_obj = Recipe
    model_connection = ShoppingCart
    response_serializer = RecipeFromTheAuthor

    def get_queryset(self):
        return self.request.user.shopping_cart

    def create(self, request, recipe_id):
        return super().create(request, recipe_id)

    def destroy(self, request, recipe_id):
        return super().destroy(request, recipe_id)


class FavoriteRecipesViewSet(CreateDestroyObjView):
    """
    Добавление/удаление из Избранного
    """
    serializer_class = FavoriteSerializer
    model_obj = Recipe
    model_connection = FavoriteRecipe
    response_serializer = RecipeFromTheAuthor

    def get_queryset(self):
        return self.request.user.favorites

    def create(self, request, recipe_id):
        return super().create(request, recipe_id)

    def destroy(self, request, recipe_id):
        return super().destroy(request, recipe_id)
