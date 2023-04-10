import json

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load data from csv file in the directory "data"'

    def handle(self, *args, **kwargs):
        with open(
            './data/ingredients.json',
            'r',
            encoding='utf-8'
        ) as file:
            reader = json.load(file)
            Ingredient.objects.bulk_create(
                [Ingredient(**data) for data in reader]
            )

        self.stdout.write(self.style.SUCCESS(
            '==>>>Ингредиенты успешно загружены в БД<<<=='
        ))
