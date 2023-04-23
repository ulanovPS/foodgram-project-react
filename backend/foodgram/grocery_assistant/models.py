from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


""" Рецепты для приготовления блюд """


class Recipes(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
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

    def __str__(self):
        return self.recipe_name


""" Теги для поиска рецепта """


class Tags(models.Model):
    tag_name = models.CharField(
        verbose_name='Тег',
        max_length=256,
        db_index=True
    )  # Название тега
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=16,
        db_index=True
    )  # Цвет тега
    slug = models.SlugField(
        max_length=20,
        db_index=True,
        verbose_name='Slag тег'
    )  # Slag тег

    def __str__(self):
        return f'{self.tag_name}'


""" Список тегов на рецепт, сводная таблица """


class Tags_list(models.Model):
    recipes_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )  # Номер рецепта
    tag_id = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )  # Номер тега


""" Единицы измерения ингридиентов """


class Unit_of_measure(models.Model):
    unit_name = models.CharField(
        verbose_name='Единица измерения',
        max_length=20,
        db_index=True
    )  # Название единицы измерения

    def __str__(self):
        return self.unit_name


""" Ингридиенты """


class Ingredients(models.Model):
    ingr_name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=256,
        db_index=True
    )  # Название ингридиента

    def __str__(self):
        return self.ingr_name


""" Список ингридиентов для рецепта с единицами измерения """


class Ingredients_list(models.Model):
    recipes_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )  # Номер рецепта
    ingr_id = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )  # Номер ингридиента
    unit_id = models.ForeignKey(
        Unit_of_measure,
        on_delete=models.CASCADE,
        verbose_name='Единицы измерения'
    )  # Единица измерения


""" Список рецептов для которых надо составить список покупок """


class Shoping_list(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )  # Пользователь
    recipes_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )  # Номер рецепта


""" Список любимых рецептов """


class Favorite_recipes(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользовтель',
    )  # Пользователь
    recipes_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )  # Номер рецепта


""" Подписка на автора рецептов """


class Follow(models.Model):
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
