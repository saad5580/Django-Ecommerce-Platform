# Generated by Django 4.2.9 on 2024-01-27 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
