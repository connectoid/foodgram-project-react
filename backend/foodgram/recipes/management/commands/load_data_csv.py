import csv

from django.core.management import BaseCommand

from recipes.models import Ingredient, User

CSV_PATH = 'static/data/'


class Command(BaseCommand):
    help = "Loads data from csv"

    def handle(self, *args, **options):

        with open('static/data/ingredients.csv', 'r', encoding='utf-8') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            for row in dict_reader:
                Ingredient.objects.get_or_create(
                    title=row['title'],
                    unit=row['unit'])

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена'))
