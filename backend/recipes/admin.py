from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class AlphabetListFilter(admin.SimpleListFilter):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщэюя'
    title = ('По алфавиту')
    parameter_name = 'alphabet'

    def lookups(self, request, model_admin):
        alpha_set = []
        for letter in self.alphabet:
            alpha_set.append((letter, (letter)))
        return alpha_set

    def queryset(self, request, queryset):
        for letter in self.alphabet:
            if self.value() == letter:
                return queryset.filter(
                    name__startswith=letter
                )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'slug', 'color']
    list_filter = ('slug', )


class TagInline(admin.TabularInline):
    model = Tag.recipes.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'is_favorited']
    list_filter = ('name', 'author', 'tags')
    exclude = ('tags', )
    inlines = [TagInline]
    readonly_fields = ['is_favorited', ]

    @admin.display(description='Кол-во добавлений в избранное')
    def is_favorited(self, obj):
        return obj.favorites.count()

    is_favorited.__name__ = 'Кол-во добавлений в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = [AlphabetListFilter, ]


@admin.register(IngredientInRecipe)
class IngredientInRecipesAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'amount']
    fields = ('recipe', ('ingredient', 'amount'))


@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user']


@admin.register(ShoppingCart)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user']
