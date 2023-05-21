from django.contrib import admin

from .models import (
    Ingredient,
    IngredientInRecipe,
    FavoriteRecipe,
    Subscribe,
    RecipeList,
    ShoppingCart,
    Tag
)

EMPTY_STRING: str = '-пусто-'
QUANTITY: int = 6


class RecipeIngredientAdmin(admin.StackedInline):
    model = IngredientInRecipe
    autocomplete_fields = ('ingredient',)


@admin.register(RecipeList)
class RecipeListAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_author', 'name', 'text',
        'cooking_time', 'get_tags', 'get_ingredients',
        'pub_date', 'get_favorite_count'
    )
    search_fields = (
        'name', 'cooking_time',
        'author__email', 'ingredients__name'
    )
    list_filter = (
        'pub_date', 'tags',
    )
    empty_value_display = EMPTY_STRING

    @admin.display(
        description='Электронная почта автора'
    )
    def get_author(self, obj):
        return obj.author.email

    @admin.display(description='Тэги')
    def get_tags(self, obj):
        tags_list = []
        for tag in obj.tags.all():
            tags_list.append(tag)
        tags_list = (', '.join([str(item) for item in tags_list]))
        return tags_list

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return '\n '.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f' {item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                'ingredient__name',
                'amount', 'ingredient__measurement_unit')])

    @admin.display(description='В избранном')
    def get_favorite_count(self, obj):
        return obj.favorite_recipe.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = EMPTY_STRING


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'measurement_unit',)
    search_fields = (
        'name', 'measurement_unit',)
    empty_value_display = EMPTY_STRING


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'author', 'created',)
    search_fields = (
        'user__email', 'author__email',)
    empty_value_display = EMPTY_STRING


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    ordering = ('user',)
    search_fields = ('recipe', 'user')
    empty_value_display = EMPTY_STRING


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    ordering = ('user',)
    search_fields = ('recipe', 'user')
    empty_value_display = EMPTY_STRING
