from posts.models import Post
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status
from likes.models import Likes
from comment.models import Comment


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

def create_public_post_like(post):
    data = {"summary": "Miller Likes Your Post!",         
            "type": "Like",
            "author_url": post.author.id,    
            "object": post.id,
            "context": "https://www.w3.org/ns/activitystreams"
            }
    return Likes.objects.create(**data)

def create_post_comment(post):

    data = {"type": "comments",  
            "comment": "Post a comment", 
            "contentType": Comment.ContentType.PLAIN_TEXT, 
            "author_url": post.author.id,
            "post": post, 
    }
    return Comment.objects.create(**data)

def create_public_comment_like(comment):
    data = {"summary": "Miller Likes Your Post!",         
            "type": "Like",
            "author_url": comment.author_url,    
            "object": comment.id,
            "context": "https://www.w3.org/ns/activitystreams"
            }
    return Likes.objects.create(**data)

class LikesTests(APITestCase):

    def setUp(self) -> None:
        self.user = create_user("SuperUser")
        self.public_post = create_public_post(self.user.author)
        self.public_post_comments = create_post_comment(self.public_post)
        self.public_post_likes = create_public_post_like(self.public_post)
        self.private_post_likes = create_public_post_like(self.public_post)
        self.public_comment_likes = create_public_comment_like(self.public_post_comments)

    def test_get_like(self):
        """ Ensure we can create a new likes object. """
        publicUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.public_post.local_id}/likes/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(publicUrl)
        self.assertEqual(publicResponse.status_code, status.HTTP_200_OK)
    
    def test_get_allLikes (self):
        publicUrl = f"/api/authors/{self.user.author.local_id}/liked/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(publicUrl)
        self.assertEqual(publicResponse.status_code, status.HTTP_200_OK)

    def test_get_commentLike(self):
        """ Ensure we can create a new likes object. """
        publicUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.public_post.local_id}/comments/{self.public_post_comments.local_id}/likes/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(publicUrl)
        self.assertEqual(publicResponse.status_code, status.HTTP_200_OK)