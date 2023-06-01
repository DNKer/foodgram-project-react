import datetime
import csv
import os

from django.core.management import BaseCommand

from recipes.models import Ingredient

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE: str = f'{DIR}/data/ingredients.csv'


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
