from typing import List

from .models import IngredientInRecipe


def create_shopping_cart(lst: List[IngredientInRecipe]) -> str:
    dct = {}
    for comp in lst:
        if comp.ingredient not in dct:
            dct[comp.ingredient] = comp.amount
        else:
            dct[comp.ingredient] = comp.amount + dct[comp.ingredient]
    shopping_list = 'Список покупок: \n\n'
    for key, value in dct.items():
        str_line = f'{key}({key.measurement_unit}) - {value},'.capitalize()
        shopping_list += str_line + '\n'
    shopping_list += '\nПриятных покупок'
    return shopping_list
