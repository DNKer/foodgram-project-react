from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """
    Модель Тэг.
    """
    name = models.CharField(
        'Название',
        max_length=60,
        unique=True,
        blank=False
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True,
        blank=False
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель Ингредиент.
    """
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        blank=False
    )
    measurement_unit = models.CharField(
        'Единица измерения ингредиента',
        max_length=200,
        blank=False
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class RecipeList(models.Model):
    """
    Модель Рецепт.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=255
    )
    image = models.ImageField(
        'Ссылка на картинку на сайте',
        upload_to='static/recipe/',
        blank=True,
        null=True
    )
    text = models.TextField(
        'Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validators.MinValueValidator(
            1, message='Минимальное время приготовления `1` минута!'), ]
        )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class IngredientInRecipe(models.Model):
    """
    Модель для количества
    ингридиентов в рецепте.
    """
    recipe = models.ForeignKey(
        RecipeList,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    amount = models.PositiveIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное количество ингридиентов `1` !'),),
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient')
        ]


class Subscribe(models.Model):
    """
    Модель Подписчик.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )
    created = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribing')
        ]

    def __str__(self):
        return (f'Пользователь {self.user} '
                f'подписан на автора {self.author}')


class FavoriteRecipe(models.Model):
    """
    Модель Избранное.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite_recipe',
        verbose_name='Пользователь')
    recipe = models.ManyToManyField(
        RecipeList,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        favorite_list=[]
        for item in self.recipe.values('name'):
            favorite_list = item['name']
        return f'Пользователь {self.user} добавил {favorite_list} в избранное.'


class ShoppingCart(models.Model):
    """
    Модель Покупка.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='Пользователь')
    recipe = models.ManyToManyField(
        RecipeList,
        related_name='shopping_cart',
        verbose_name='Покупка')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']

    def __str__(self):
        for item in self.recipe.values('name'):
            list = item['name']
        return f'Пользователь {self.user} добавил {list} в покупки.'
