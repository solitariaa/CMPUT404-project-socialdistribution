# Generated by Django 4.0.2 on 2022-02-16 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contentType',
            field=models.CharField(choices=[('text/markdown', 'Common Mark'), ('text/plain', 'Plain Text'), ('application/base64', 'Base64'), ('image/png;base64', 'Png'), ('image/jpeg;base64', 'Jpeg')], max_length=350),
        ),
        migrations.AlterField(
            model_name='post',
            name='origin',
            field=models.URLField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.URLField(blank=True, max_length=350),
        ),
    ]
