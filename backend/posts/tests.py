from posts.models import Post
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status


def create_user(username):
    user = User.objects.create_user(username=username, password="test", email=f"{username}@gmail.com")
    user.is_superuser = True
    user.is_staff = True
    user.author.verified = True
    user.author.save()
    user.save()
    return user


def create_public_post(author):
    data = {"title": "Public Post Title",
            "description": "Public Post Description",
            "contentType": Post.ContentType.PLAIN_TEXT,
            "content": "Public Post Content",
            "author": author,
            "categories": ["public", "post", "test"],
            "visibility": "PUBLIC",
            "unlisted": False
            }
    return Post.objects.create(**data)


def create_friend_post(author):
    data = {"title": "Friend Post Title",
            "description": "Friend Post Description",
            "contentType": Post.ContentType.PLAIN_TEXT,
            "content": "Friend Post Content",
            "author": author,
            "categories": ["friend", "post", "test"],
            "visibility": "FRIENDS",
            "unlisted": False
            }
    return Post.objects.create(**data)


class PostsTests(APITestCase):

    def setUp(self) -> None:
        self.user = create_user("SuperUser")
        self.public_post = create_public_post(self.user.author)
        self.friend_post = create_friend_post(self.user.author)

    def test_get_post(self):
        """ Ensure we can create a new post object. """
        publicUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.public_post.local_id}/"
        friendUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.friend_post.local_id}/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(publicUrl)
        friendResponse = self.client.get(friendUrl)
        self.assertEqual(friendResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(publicResponse.status_code, status.HTTP_200_OK)

    def test_put_post(self):
        """ Ensure we can create a new post object. """
        publicUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.public_post.local_id}/"
        friendUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.friend_post.local_id}/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(publicUrl)
        friendResponse = self.client.get(friendUrl)
        publicResponse.data["title"] = "Testing post title"
        friendResponse.data["title"]= "Testing post title"
        publicNewResponse = self.client.put(publicUrl, data=publicResponse.data, format='json')
        friendNewResponse = self.client.put(friendUrl, data=friendResponse.data, format='json')
        self.assertEqual(friendNewResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(publicNewResponse.status_code, status.HTTP_200_OK)
        publicResponse = self.client.get(publicUrl)
        friendResponse = self.client.get(friendUrl)
        self.assertEqual(friendResponse.data["title"], "Testing post title")
        self.assertEqual(publicResponse.data["title"], "Testing post title")


    def test_delete_post(self):
        """ Ensure we can create a new post object. """
        publicUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.public_post.local_id}/"
        friendUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.friend_post.local_id}/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.delete(publicUrl)
        friendResponse = self.client.delete(friendUrl)
        self.assertEqual(friendResponse.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(publicResponse.status_code, status.HTTP_204_NO_CONTENT)
