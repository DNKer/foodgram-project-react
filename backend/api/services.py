from django.db.models import F, Sum

from recipes.models import IngredientInRecipe


def collect_shopping_cart(request):
    """
    Формирование корзины (списка) покупок.
    """
    shopping_list = IngredientInRecipe.objects.filter(
        recipe__shopping_cart__user=request.user).values(
        name=F('ingredient__name'),
        measurement_unit=F('ingredient__measurement_unit')
        ).annotate(total_amount=Sum('amount'))
    text = '\n'.join([f'{0} ({1}) \u2014 {2}'.format(
                item['name'], item['measurement_unit'],
                item['total_amount'])
        for item in shopping_list])
    return text
