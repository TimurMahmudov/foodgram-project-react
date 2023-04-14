from rest_framework.routers import DefaultRouter

from .recipes_views import (FavoriteRecipesViewSet, IngredientViewSet,
                            RecipeViewSet, ShoppingCartViewSet, TagViewSet)
from .users_views import CreateDestroySubscribeViewSet, CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'users',
                   CustomUserViewSet,
                   basename='users')
router_v1.register(r'recipes',
                   RecipeViewSet,
                   basename='recipes')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                   ShoppingCartViewSet,
                   basename='shopping_cart')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                   FavoriteRecipesViewSet,
                   basename='favorite')
router_v1.register(r'users/(?P<user_id>\d+)/subscribe',
                   CreateDestroySubscribeViewSet,
                   basename='subscribe')
