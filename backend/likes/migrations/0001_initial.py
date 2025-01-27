# Generated by Django 4.0.2 on 2022-03-19 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Like', max_length=100)),
                ('author_url', models.URLField(max_length=250)),
                ('summary', models.TextField()),
                ('context', models.URLField()),
                ('object', models.URLField(max_length=250)),
            ],
        ),
    ]
