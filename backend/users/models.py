from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'


class User(AbstractUser):
    ROLES = ((USER, USER), (ADMIN, ADMIN))

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,)

    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        db_index=True,
        unique=True,
        help_text='Введите адрес электронной почты'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Введите имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Введите фамилию'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    @property
    def is_user(self):
        return self.is_user

    def __str__(self):
        return f'@{self.username}: {self.email}.'


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

    def get_email_field_name(self):
        return self.author.email
