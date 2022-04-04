from posts.models import Post
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status
from notifications.models import Notification


def create_user(username):
    user = User.objects.create_user(username=username, password="test", email=f"{username}@gmail.com")
    user.is_superuser = True
    user.is_staff = True
    user.author.verified = True
    user.author.save()
    user.save()
    return user

def create_followed_user(username):
    user = User.objects.create_user(username=username, password="test", email=f"{username}@gmail.com")
    user.is_superuser = True
    user.is_staff = True
    user.author.verified = True
    user.author.save()
    user.save()
    return user


def create_post_notification(actor, author):
    data = {
            "type": Notification.ContentType.FOLLOW_REQUEST,
            "author": author, 
            "actor": actor,
            "summary": "Post notification",
            }
    return Notification.objects.create(**data)

class NotificationTests(APITestCase):

    def setUp(self) -> None:
        self.user = create_user("SuperUser")
        self.followed_user = create_followed_user("Tester")
        self.post_notification = create_post_notification(self.followed_user.author, self.user.author)


    def test_get_notifications(self):
        """ Ensure we can create a new notification object. """
        retrievedUrl = f"/api/authors/{self.followed_user.author.local_id}/notifications/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(retrievedUrl)
        self.assertEqual(publicResponse.status_code, status.HTTP_200_OK)

    def test_delete_notifications(self):
        deleteUrl = f"/api/authors/{self.user.author.local_id}/notifications/{self.post_notification.id}/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.delete(deleteUrl)
        self.assertEqual(publicResponse.status_code, status.HTTP_204_NO_CONTENT)
