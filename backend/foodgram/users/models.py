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
    )  # email пользователя, применяется для ввхода
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True,
    )  # Логин
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True,
    )  # Имя пользователя
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
    )  # Фамилия пользователя
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )  # Роль пользователя
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )  # Пароль пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username
