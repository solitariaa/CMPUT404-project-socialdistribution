# Generated by Django 4.0.2 on 2022-02-13 03:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('local_id', models.UUIDField(primary_key=True, serialize=False)),
                ('id', models.URLField(max_length=350)),
                ('host', models.URLField()),
                ('displayName', models.CharField(max_length=100)),
                ('github', models.URLField(default='', max_length=350)),
                ('profileImage', models.URLField(default='https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png', max_length=350)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
