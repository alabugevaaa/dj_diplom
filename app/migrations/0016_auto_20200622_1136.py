# Generated by Django 2.2.13 on 2020-06-22 02:36

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200622_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(max_length=250, storage=django.core.files.storage.FileSystemStorage(location=None), upload_to='img', verbose_name='Фото'),
        ),
    ]