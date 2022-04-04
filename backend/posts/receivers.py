from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Post
from authors.models import Author
from .serializers import PostSerializer
import json
from inbox.models import InboxItem
from concurrent.futures import ThreadPoolExecutor
from authors.serializers import AuthorSerializer
from nodes.models import Node
from backend import helpers
from authors.helpers import get_all_authors
from rest_framework.exceptions import APIException

class AuthorNotFound(APIException):
    """This exception raises a 409 error in the event that a transaction could not be completed"""
    status_code = 404
    default_detail = 'Receiving Author Not Found!'
    default_code = 'author_not_found'


@receiver(post_save, sender=Post)
def on_create_post(sender, **kwargs):
    """This task populates the ID field with the local id of a new post"""
    if kwargs.get('created'):
        # Save The ID
        post: Post = kwargs.get('instance')
        url = f"{settings.DOMAIN}/authors/{post.author.local_id}/posts/{post.local_id}/"
        post.id = url
        post.source = url if not post.source else post.source
        post.origin = url if not post.origin else post.origin

        # Push Posts To Recipient's Inbox
        if post.contentType != post.ContentType.PNG and post.contentType != post.ContentType.JPEG:
            data = PostSerializer(post).data
            data["author"] = AuthorSerializer(post.author).data
            if post.visibility == "PUBLIC":
                # Get List Of Remote Authors
                authors = []
                nodes = Node.objects.all()
                with ThreadPoolExecutor(max_workers=1) as executor:
                    futures = executor.map(lambda node: helpers.get_authors(node.host), nodes)
                for future in futures:
                    if "items" in future:
                        authors += future["items"]

                # Push To Author's Inbox
                authors = list(map(lambda author: helpers.extract_inbox_url(author), authors))
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.map(lambda author: helpers.post(author, json.dumps(data), headers={"Content-Type": "application/json"}), authors)

            elif post.visibility == "FRIENDS":
                followers = [follower.actor for follower in post.author.follower_set.all()] + [post.author.id]
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.map(lambda follower: helpers.post(f"{follower.rstrip('/')}/inbox/", json.dumps(data), headers={"Content-Type": "application/json"}), followers)
            else:
                # Get All Authors
                authors = get_all_authors()

                # Find The Matching Author
                found = False
                for author in authors:
                    #print("Recipient:", post.visibility.rstrip("/"))
                    #print("Author:", author["id"].rstrip("/"))
                    #print("Found:",author["id"].rstrip("/") == post.visibility.rstrip("/"))
                    if author["id"].rstrip("/") == post.visibility.rstrip("/"):
                        helpers.post(f"{post.visibility.rstrip('/')}/inbox/", json.dumps(data), headers={"Content-Type": "application/json"})
                        found = True
                        break

                # If The Recipient Was Not Found, Delete The Post
                if not found:
                    post.delete()
                    raise AuthorNotFound()

                # If The Recipient Was Found, Send Post To Author's Inbox
                if post.visibility.rstrip('/') != post.author.id.rstrip('/'):
                    helpers.post(f"{post.author.id.rstrip('/')}/inbox/", json.dumps(data), headers={"Content-Type": "application/json"})

        # Save The Post
        post.save()


@receiver(post_delete, sender=Post)
def on_delete_post(sender, **kwargs):
    """WHen A Post Is Deleted, We Want To Delete All Matching Inbox Items"""
    post: Post = kwargs.get('instance')
    InboxItem.objects.filter(src=post.id).delete()

    if post.contentType == post.ContentType.COMMON_MARK:
        references = post.content.split("(")[1].split("image/)")[0]
        Post.objects.filter(id=references).delete()
