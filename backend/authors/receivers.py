from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Author, Avatar
from django.contrib.auth.models import User
from django.conf import settings


@receiver(post_save, sender=User)
def on_create_profile(sender, **kwargs):
    """This task creates a new author in the database whenever a new user profile is created"""
    if kwargs.get('created'):
        user: User = kwargs.get('instance')
        Author.objects.create(id="", host=f"{settings.DOMAIN}/", displayName=f"{user.username}", profile=user)


@receiver(post_save, sender=Author)
def on_create_author(sender, **kwargs):
    """This task populates the ID field with the local id of a new author"""
    if kwargs.get('created'):
        # Set Author ID
        author: Author = kwargs.get('instance')
        author.id = f"{settings.DOMAIN}/authors/{author.local_id}/"

        # Create Avatar
        avatar: Avatar = Avatar(author=author)
        author.profileImage = f"{settings.DOMAIN}/api/authors/{author.local_id}/avatar/"
        avatar.save()

        # Save Author
        author.save()


@receiver(post_delete, sender=Author)
def on_delete_author(sender, **kwargs):
    """This task deletes the profile when an author is deleted"""
    author: Author = kwargs.get('instance')
    author.profile.delete()
