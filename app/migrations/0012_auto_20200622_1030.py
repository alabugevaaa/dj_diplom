# Generated by Django 2.2.13 on 2020-06-22 01:30

import ckeditor_uploader.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_review_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order',
        ),
        migrations.AlterField(
            model_name='article',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания статьи'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления отзыва'),
        ),
    ]