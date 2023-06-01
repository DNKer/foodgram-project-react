import csv
import datetime
from pathlib import Path

from django.core.management import BaseCommand

from recipes.models import Ingredient


FILE: str = 'recipes/data/ingredients.csv'


def import_csv_data() -> None:
    """ Обработка файла csv. """
    with open(FILE, 'r', encoding='UTF-8') as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            name, measurement_unit = row
            Ingredient.objects.get_or_create(
                name=name,
                measurement_unit=measurement_unit)
        csvfile.close()


class Command(BaseCommand):
    """ Загрузка данных из csv файла. """
    help = ('Загрузка данных из /data/ingredients.csv.'
            'Запуск: python manage.py load_data.')

    def handle(self, *args, **options) -> None:
        start_time = datetime.datetime.now()
        try:
            import_csv_data()
        except Exception as error:
            self.stdout.write(
                self.style.WARNING(f'Сбой в работе импорта: {error}.')
            )
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Загрузка данных завершена за '
                f' {(datetime.datetime.now() - start_time).total_seconds()} '
                f'сек.')
            )
