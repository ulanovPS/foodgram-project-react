# Generated by Django 3.2.18 on 2023-05-17 17:42

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Любимые рецепты',
                'verbose_name_plural': 'Любимые рецепты',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Подписки на автора',
                'verbose_name_plural': 'Подписки на автора',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название ингридиента')),
                ('measurement_unit', models.CharField(blank=True, max_length=20, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name_plural': 'Ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение >= 1')], verbose_name='Колличество ингридиента')),
            ],
            options={
                'verbose_name_plural': 'Список ингридиентов',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Рецепт')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/', verbose_name='Картинка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.IntegerField(verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Тег')),
                ('color', models.CharField(max_length=16, verbose_name='Цвет тега в HEX формате')),
                ('slug', models.SlugField(max_length=20, unique=True, verbose_name='Slag тег')),
            ],
            options={
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='ShopingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoping_list', to='grocery_assistant.recipe')),
            ],
            options={
                'verbose_name_plural': 'Список покупок',
            },
        ),
    ]
