import base64

from django.core.files.base import ContentFile
from django.db.models import Sum
from django.http import HttpResponse
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
            'ingredient__name',
            'ingredient__measurement_unit',).annotate(
            value=Sum('amount')).order_by('ingredient__name')
    response = HttpResponse(
        content_type='text/plain',
        charset='utf-8',)
    response['Content-Disposition'] = (
        'attachment; filename=shopping_cart.txt')
    response.write('Список продуктов к покупке:\n')
    for ingredient in shopping_list:
        response.write(
            f'- {ingredient["ingredient__name"]} '
            f'- {ingredient["value"]} '
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )
    return response
