# Generated by Django 3.2.18 on 2023-04-26 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_assistant', '0007_recipes_ingredients_lists'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='tags_lists',
            field=models.ManyToManyField(through='grocery_assistant.Tags_list', to='grocery_assistant.Tags'),
        ),
    ]
