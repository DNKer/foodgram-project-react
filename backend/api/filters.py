from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import RecipeList


class IngredientFilter(SearchFilter):
    """
    Поиск по имени Ингредиента.
    """
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    """
    Фильтр для Рецепта.
    """
    author = filters.NumberFilter()
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_in_shopping_cart')

    class Meta:
        model = RecipeList
        fields = ['tags', 'author', ]

    def filter_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
