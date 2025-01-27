# Generated by Django 4.0.2 on 2022-03-04 11:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0003_alter_author_github'),
        ('posts', '0003_post_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('type', models.CharField(default='comments', max_length=100)),
                ('comment', models.TextField()),
                ('contentType', models.CharField(choices=[('text/markdown', 'Common Mark'), ('text/plain', 'Plain Text'), ('application/base64', 'Base64'), ('image/png;base64', 'Png'), ('image/jpeg;base64', 'Jpeg')], max_length=350)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('local_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.CharField(blank=True, default='post', max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.author')),
                ('post', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]
