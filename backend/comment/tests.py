from django.test import TestCase
from comment.models import Comment
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
from posts.models import Post


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
            "visibility": Post.Visibility.PUBLIC,
            "unlisted": False
            }
    return Post.objects.create(**data)

def create_post_comment(post):

    data = {"type": "comments",  
            "comment": "Post a comment", 
            "contentType": Comment.ContentType.PLAIN_TEXT, 
            "author_url": post.author.id,
            "post": post, 
    }
    return Comment.objects.create(**data)





