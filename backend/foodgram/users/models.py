from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Кастомизация модели User """
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
