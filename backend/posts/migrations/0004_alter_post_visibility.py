# Generated by Django 4.0.2 on 2022-03-22 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', 'Public'), ('FRIENDS', 'Friends'), ('PRIVATE', 'Private')], max_length=100),
        ),
    ]
