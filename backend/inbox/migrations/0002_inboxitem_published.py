# Generated by Django 4.0.2 on 2022-02-23 14:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inboxitem',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
