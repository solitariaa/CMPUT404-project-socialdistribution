# Generated by Django 4.0.2 on 2022-03-17 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_notification_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('Follow', 'Follow Request'), ('Comment', 'Comment'), ('Like', 'Like')], max_length=100),
        ),
    ]
