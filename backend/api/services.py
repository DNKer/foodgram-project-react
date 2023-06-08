import base64

from django.core.files.base import ContentFile
from django.db.models import F, Sum
from rest_framework import serializers

from recipes.models import IngredientInRecipe


class Base64ImageField(serializers.ImageField):
    """
    Декодируем изображение.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


def collect_shopping_cart(user):
    """
    Формирование корзины (списка) покупок.
    """
    shopping_list = IngredientInRecipe.objects.filter(
        recipe__shopping_cart__user=user).values(
        name=F('ingredient__name'),
        measurement_unit=F('ingredient__measurement_unit')).annotate(
        total_amount=Sum('amount'))
    for item in shopping_list:
        text = '\n'.join(f'{0} ({1}) \u2014 {2}'.format(
            item['name'], item['measurement_unit'],
            item['total_amount']))
    return text
