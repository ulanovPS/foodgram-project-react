from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Кастомизация модели User """
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'User'),
        (ADMIN, 'Administrator')
    ]
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
