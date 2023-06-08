import datetime
import json

from django.core.management import BaseCommand

from recipes.models import Ingredient


FILE: str = 'data/ingredients.json'


def import_csv_data() -> None:
    """ Обработка файла csv. """
    with open(FILE, 'r') as file:
        data = json.load(file)
        for note in data:
            Ingredient.objects.get_or_create(**note)
    return None


class Command(BaseCommand):
    """ Загрузка данных из csv файла. """
    help = ('Загрузка данных из /data/ingredients.json.'
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
