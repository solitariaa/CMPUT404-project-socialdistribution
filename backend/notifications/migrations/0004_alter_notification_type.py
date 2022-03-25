# Generated by Django 4.0.2 on 2022-03-22 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_alter_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('Follow', 'Follow Request'), ('Comment', 'Comment'), ('Like', 'Like'), ('Post', 'Post')], max_length=100),
        ),
    ]