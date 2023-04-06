from rest_framework.routers import SimpleRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

recipe_router = SimpleRouter()
recipe_router.register(r'recipes', RecipeViewSet, basename='recipes')
recipe_router.register(r'tags', TagViewSet)
recipe_router.register(r'ingredients', IngredientViewSet)
