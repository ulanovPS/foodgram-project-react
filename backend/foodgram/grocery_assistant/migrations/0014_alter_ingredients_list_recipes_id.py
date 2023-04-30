# Generated by Django 3.2.18 on 2023-04-30 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_assistant', '0013_alter_ingredients_list_ingr_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients_list',
            name='recipes_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='grocery_assistant.recipes', verbose_name='Рецепт'),
        ),
    ]
