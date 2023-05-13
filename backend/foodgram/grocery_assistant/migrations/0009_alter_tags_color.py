# Generated by Django 3.2.18 on 2023-05-13 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_assistant', '0008_alter_tags_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='color',
            field=models.CharField(choices=[('Black', '000000'), ('Ginger', 'ffa500')], db_index=True, default=('Black', '000000'), max_length=16, unique=True, verbose_name='Цвет тега'),
        ),
    ]
