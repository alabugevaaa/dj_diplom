# Generated by Django 2.2.10 on 2020-06-17 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200617_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='points',
            field=models.IntegerField(default=0, verbose_name='Оценка'),
        ),
    ]
