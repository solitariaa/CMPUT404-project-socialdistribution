# Generated by Django 4.0.2 on 2022-03-21 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='author_url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='likes',
            name='context',
            field=models.URLField(default='https://www.w3.org/ns/activitystreams'),
        ),
    ]