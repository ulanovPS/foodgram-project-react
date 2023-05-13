# Generated by Django 3.2.18 on 2023-05-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_assistant', '0009_alter_tags_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='color',
            field=models.CharField(choices=[('000000', 'Black'), ('ffa500', 'Ginger')], db_index=True, default=('000000', 'Black'), max_length=16, unique=True, verbose_name='Цвет тега'),
        ),
    ]
