# Generated by Django 2.2.16 on 2022-07-22 23:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#569914', max_length=7, validators=[django.core.validators.RegexValidator(message='Укажите цвет в HEX кодировке.', regex='#[a-f\\d]{6}')], verbose_name='Цвет в HEX'),
        ),
    ]
