from django.test import TestCase
from comment.models import Comment
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
from posts.models import Post
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

def create_post_comment(post):

    data = {"type": "comments",  
            "comment": "Post a comment", 
            "contentType": Comment.ContentType.PLAIN_TEXT, 
            "author_url": post.author.id,
            "post": post, 
    }
    return Comment.objects.create(**data)


class CommentsTests(APITestCase):

    def setUp(self) -> None:
        self.user = create_user("SuperUser")
        self.public_post = create_public_post(self.user.author)
        self.public_post_comments = create_post_comment(self.public_post)
        

    def test_get_comment(self):
        """ Ensure we can create a new comment object. """
        publicUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.public_post.local_id}/comments/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(publicUrl)
        self.assertEqual(publicResponse.status_code, status.HTTP_200_OK)

    def test_edit_comment(self):
        """ Ensure we can edit a new comment. """
        publicUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.public_post.local_id}/comments/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(publicUrl)
        publicResponse.data["comments"][0]['comment'] = "Edit a comment"
        tempUrl = publicResponse.data["comments"][0]['id'].replace('http://127.0.0.1:8000/','')
        patchUrl = f"/api/{tempUrl}"
        publicNewResponse = self.client.patch(patchUrl, data=publicResponse.data, format='json')
        self.assertEqual(publicNewResponse.status_code, status.HTTP_200_OK)
        retrieveResponse = self.client.get(patchUrl)
        print (retrieveResponse.data)

    def test_delete_comment(self):
        """ Ensure we can edit a new comment. """
        publicUrl = f"/api/authors/{self.user.author.local_id}/posts/{self.public_post.local_id}/comments/"
        self.client.force_authenticate(user=self.user)
        publicResponse = self.client.get(publicUrl)
        publicResponse.data["comments"][0]['comment'] = "Edit a comment"
        tempUrl = publicResponse.data["comments"][0]['id'].replace('http://127.0.0.1:8000/','')
        deleteUrl = f"/api/{tempUrl}"
        publicNewResponse = self.client.delete(deleteUrl)
        self.assertEqual(publicNewResponse.status_code, status.HTTP_204_NO_CONTENT)
        retrieveResponse = self.client.get(publicUrl)
        self.assertEqual(retrieveResponse.data["comments"], []) 
        