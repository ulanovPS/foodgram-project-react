# Generated by Django 3.2.18 on 2023-04-26 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='username_is_not_me',
        ),
    ]