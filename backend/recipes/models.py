from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """
    Теги
    """
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Введите название тега')
    color = ColorField(verbose_name='Выберите цвет')
    slug = models.SlugField(db_index=True, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name', )
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ингредиенты
    """
    name = models.CharField(max_length=100,
                            db_index=True,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=50,
                                        verbose_name='Единица измерения')

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Рецепты
    """
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name='Автор',
                               related_name='recipes')
    name = models.CharField(max_length=100,
                            db_index=True,
                            verbose_name='Название рецепта')
    image = models.ImageField(upload_to='фото_рецептов',
                              verbose_name='Фото рецепта')
    text = models.TextField(verbose_name='Описание приготовления рецепта')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Теги')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe')

    class Meta:
        ordering = ('name', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """
    Связь между рецептами и ингредиентами
    """
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredient',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='recipe_ingredient',
                                   verbose_name='Название ингредиента')
    amount = models.PositiveIntegerField(verbose_name='Кол-во для рецепта')

    class Meta:
        ordering = ('recipe', )
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class FavoriteRecipe(models.Model):
    """
    Избранное
    """
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorites',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь')

    class Meta:
        ordering = ('user', )
        verbose_name = 'В Избранном у пользователя'
        verbose_name_plural = 'В Избранном у пользователей'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} у {self.user}'


class ShoppingCart(models.Model):
    """
    Список покупок
    """
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping_cart',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart',
                             verbose_name='Пользователь')

    class Meta:
        ordering = ('user', )
        verbose_name = 'В списке покупок у пользователя'
        verbose_name_plural = 'В списках покупок у пользователей'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe} у {self.user}'
