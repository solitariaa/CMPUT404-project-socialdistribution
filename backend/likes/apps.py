from django.apps import AppConfig


class LikesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'likes'


class LikedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'liked'
