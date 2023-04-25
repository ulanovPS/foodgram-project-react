# Generated by Django 3.2.18 on 2023-04-23 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_assistant', '0003_auto_20230421_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients_list',
            name='ingr_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_assistant.ingredients', verbose_name='Ингридиент'),
        ),
        migrations.AlterField(
            model_name='ingredients_list',
            name='recipes_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_assistant.recipes', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='ingredients_list',
            name='unit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_assistant.unit_of_measure', verbose_name='Единицы измерения'),
        ),
    ]