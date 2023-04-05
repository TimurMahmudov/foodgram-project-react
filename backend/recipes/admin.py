from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient,IngredientInRecipe,
                     Recipe, ShoppingCart, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
