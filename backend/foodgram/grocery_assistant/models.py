from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

from .validators import HexColorValidator


class Tag(models.Model):
    """ Теги для поиска рецепта """
    color_validator = HexColorValidator()

    name = models.CharField(
        verbose_name='Тег',
        max_length=256,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет тега в HEX формате',
        max_length=16,
        validators=[color_validator],
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name='Slag тег',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """ Ингридиенты """
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=256,
        unique=True,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        blank=True,
        max_length=20,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ингридиенты'


class Recipe(models.Model):
    """ Рецепты для приготовления блюд """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='author_recipes'
    )
    name = models.CharField(
        verbose_name='Рецепт',
        max_length=256,
        db_index=True
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='image/',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name="Ингридиент"
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Таг"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date', 'name']


class IngredientRecipe(models.Model):
    """ Список ингридиентов для рецепта с единицами измерения """
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes_list'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        related_name='ingredients_lists'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Колличество ингридиента',
        validators=[
            MinValueValidator(
                1,
                'Минимальное значение >= 1'
            )
        ],
    )

    class Meta:
        verbose_name_plural = 'Список ингридиентов'

    def __str__(self):
        return f'{self.recipes} {self.ingredient}'


class ShopingList(models.Model):
    """ Список рецептов для которых надо составить список покупок """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoping_list'
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoping_list'
    )

    class Meta:
        verbose_name_plural = 'Список покупок'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipes'],
            name='unique_cart')]


class FavoriteRecipe(models.Model):
    """ Список любимых рецептов """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользовтель',
        related_name='favorite'
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite'
    )

    class Meta:
        verbose_name_plural = 'Любимые рецепты'
        verbose_name = 'Любимые рецепты'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipes'],
            name='%(app_label)s_%(class)s_unique')]


class Follow(models.Model):
    """ Подписка на автора рецептов """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )

    class Meta:
        verbose_name_plural = 'Подписки на автора'
        verbose_name = 'Подписки на автора'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='%(app_label)s_%(class)s_unique')
        ]

        def __str__(self):
            return f'Пользователь {self.user} подписан на {self.author}'
