from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Уникальное имя пользователя',
        max_length=150,
        db_index=True,
        unique=True,
        blank=False,
        help_text='Введите уникальное имя пользователя'
    )    
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        db_index=True,
        unique=True,
        blank=False,
        help_text='Введите адрес электронной почты'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        help_text='Введите имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        help_text='Введите фамилию'
    )
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.email
