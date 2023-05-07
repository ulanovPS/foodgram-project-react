from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tags(models.Model):
    """ Теги для поиска рецепта """
    tag_name = models.CharField(
        verbose_name='Тег',
        max_length=256,
        db_index=True,
        unique=True,
    )  # Название тега
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=16,
        db_index=True,
        unique=True,
    )  # Цвет тега
    slug = models.SlugField(
        max_length=20,
        db_index=True,
        verbose_name='Slag тег',
        unique=True,
    )  # Slag тег

    def __str__(self):
        return f'{self.tag_name}'

    class Meta:
        verbose_name_plural = 'Теги'


class Ingredients(models.Model):
    """ Ингридиенты """
    ingr_name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=256,
        db_index=True
    )  # Название ингридиента
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        blank=True,
        max_length=20,
        db_index=True
    )

    def __str__(self):
        return self.ingr_name

    class Meta:
        verbose_name_plural = 'Ингридиенты'


class Recipes(models.Model):
    """ Рецепты для приготовления блюд """
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='author_recipes'
    )  # Автор рецепта
    recipe_name = models.CharField(
        verbose_name='Рецепт',
        max_length=256,
        db_index=True
    )  # Название рецепта
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='image/',
        null=True,
        blank=True
    )  # Картинка рецепта
    description = models.TextField(
        verbose_name='Описание'
    )  # Описание рецепта
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )  # Время приготовления рецепта
    public_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )  # Дата публикации рецепта
    ingredients_lists = models.ManyToManyField(
        Ingredients,
        through='Ingredients_list'
    )
    tags = models.ManyToManyField(
        Tags,
    )

    def __str__(self):
        return self.recipe_name

    class Meta:
        verbose_name_plural = 'Рецепты'
        ordering = ['-public_date', 'recipe_name']


class Ingredients_list(models.Model):
    """ Список ингридиентов для рецепта с единицами измерения """
    recipes_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes_list'
    )  # Номер рецепта
    ingr_id = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        related_name='ingredients_lists'
    )  # Номер ингридиента
    quantity = models.PositiveSmallIntegerField(
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
        return f'{self.recipes_id} {self.ingr_id}'


class Shoping_list(models.Model):
    """ Список рецептов для которых надо составить список покупок """
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shoping_list'
    )  # Пользователь
    recipes_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipes_shoping_list'
    )  # Номер рецепта

    class Meta:
        verbose_name_plural = 'Список покупок'


class Favorite_recipes(models.Model):
    """ Список любимых рецептов """
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользовтель',
        related_name='user_favorite_recipes'
    )  # Пользователь
    recipes_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes_favorite'
    )  # Номер рецепта

    class Meta:
        verbose_name_plural = 'Любимые рецепты'


class Follow(models.Model):
    """ Подписка на автора рецептов """
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )  # Пользователь
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )  # Пользователь, автор рецепта

    class Meta:
        verbose_name_plural = 'Подписки на автора'
