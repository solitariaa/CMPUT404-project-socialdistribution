import imp
from posts.models import Post
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status
from followers.models import Follower, Following


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

def create_Follower(actor, author):
    data = {
            "object": author, 
            "actor": actor,
            "summary": "A wants to follow B",
            }
    return Follower.objects.create(**data)

def create_Following (actor, author):
    data = {
            "author": author,
            "follows": actor,
            }
    return Following.objects.create(**data)

class FollowersTests(APITestCase):

    def setUp(self) -> None:
        self.user = create_user("SuperUser")
        self.testuser = create_followed_user("Tester")
        self.follower = create_Follower( self.testuser.author, self.user.author)
        self.following = create_Following( self.testuser.author, self.user.author)
    
    # def test_get_followers (self):
    #     publicUrl = f"/api/authors/{self.user.author.local_id}/followers/"
    #     self.client.force_authenticate(user=self.user)
    #     publicResponse = self.client.get(publicUrl)
    #     print (publicResponse)

    # def test_get_following (self):
    #     publicUrl = f"/api/authors/{self.user.author.local_id}/following/"
    #     self.client.force_authenticate(user=self.user)
    #     publicResponse = self.client.get(publicUrl)
        # print (publicResponse)
