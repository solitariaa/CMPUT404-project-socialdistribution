# Generated by Django 4.0.2 on 2022-03-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0003_alter_likes_author_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='author_url',
            field=models.CharField(max_length=250),
        ),
    ]
