from rest_framework.parsers import JSONParser
from likes.models import Likes
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .models import InboxItem
from notifications.models import Notification
from comment.models import Comment
from comment.serializers import CommentSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from .serializers import InboxItemSerializer
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from concurrent.futures import ThreadPoolExecutor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from authors.models import Author
from backend.permissions import IsOwnerOrAdmin
from backend import helpers
from nodes.models import Node


class IsInboxOwnerOrAdmin(IsOwnerOrAdmin):
    """Only Allow Owners Or Admins To Access The Object"""

    @staticmethod
    def get_owner(obj):
        return obj.owner.profile


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data, **kwargs):
        return Response({'type': "inbox", 'author': kwargs["author"], 'items': data})


class InboxItemList(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    serializer_class = InboxItemSerializer
    pagination_class = CustomPageNumberPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    parser_classes = [JSONParser]

    def list(self, request, *args, **kwargs):
        # Fetch The Owner
        owner = get_object_or_404(Author, local_id=self.kwargs["author"])

        # Get All Local Inbox Items
        local_items = [item for item in owner.inboxitem_set.filter(src__contains=settings.DOMAIN.rstrip("/"))]
        local_friend_posts = [PostSerializer(post).data for post in Post.objects.filter(id__in=[x.src for x in local_items]).exclude(visibility="PUBLIC")]
        for item, post in zip(local_items, local_friend_posts):
            post["description"] = item.tag if item.tag != "" else post["description"]

        # Get All Remote Inbox Items
        remote_friend_items = [item for item in owner.inboxitem_set.exclude(src__contains=settings.DOMAIN.rstrip("/"))]
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.map(lambda x: helpers.get(x), [x.src for x in remote_friend_items])
        remote_friend_posts = [p.json() for p in future if p.status_code == 200]
        for item, post in zip(remote_friend_items, remote_friend_posts):
            post["description"] = item.tag if item.tag != "" else post["description"]
            post["visibility"] = "FRIENDS"

        # Get All Local Public Posts
        local_public_posts = [PostSerializer(post).data for post in Post.objects.filter(id__contains=settings.DOMAIN.rstrip("/"), visibility="PUBLIC")]

        # Get List Of Remote Authors
        authors = []
        nodes = Node.objects.all()
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = executor.map(lambda node: helpers.get_authors(node), [node.host for node in nodes if node.host.rstrip("/") not in settings.DOMAIN.rstrip("/")])
        for future in futures:
            if "items" in future:
                authors += future["items"]
            elif "authors" in future:
                authors += future["authors"]

        # Get Posts From Remote Authors
        urls = [helpers.extract_posts_url(author) for author in authors]
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = executor.map(lambda url: helpers.get(url), urls)
        remote_public_posts = []
        for f in futures:
            if f is not None and f.status_code == 200 and "application/json" in f.headers.get("Content-Type", ""):
                if "posts" in f.json():
                    remote_public_posts += f.json()["posts"]
                elif "items" in f.json():
                    remote_public_posts += f.json()["items"]

        # Validate Posts
        posts = local_friend_posts + local_public_posts + remote_friend_posts + remote_public_posts
        for post in posts:
            helpers.validate_post(post)
        posts = [post for post in posts if "content" in post and len(post["content"]) < 500]

        # Paginate Response
        posts.sort(key=lambda x: x.get("published", '2022-03-24T18:22:07.990808-06:00'), reverse=True)
        posts = list(filter(lambda x: "image" not in x["contentType"], posts))
        page = self.paginator.paginate_queryset(posts, request)

        # Return Response
        return self.paginator.get_paginated_response(page, author=owner.local_id)

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        author = get_object_or_404(Author, local_id=kwargs["author"])
        if request.data["type"].lower() == "post":
            if request.data["visibility"].lower() != "public":
                inbox_item = InboxItem(owner=author, src=request.data["id"], tag=request.data.get("description", ""))
                inbox_item.save()
                return Response(InboxItemSerializer(inbox_item).data, status=status.HTTP_201_CREATED)
            return Response({"ok": "Successfully Posted To Inbox!"}, status=status.HTTP_200_OK)
        elif request.data["type"].lower() == "follow":
            if "actor" in request.data and "displayName" in request.data["actor"] and "url" in request.data["actor"]:
                summary = f"{request.data['actor']['displayName']} Wants To Follow You!"
                notification = Notification(type="Follow", author=author, actor=request.data["actor"]["url"], summary=summary)
                notification.save()
                return Response({"success": "Follow Request Delivered!"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid Follow Object Received!"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data["type"].lower() == "like":
            if "author" in request.data and "id" in request.data["author"] and "summary" in request.data:
                # Save Like
                request.data.pop("@context", "")
                sender = request.data.pop("author")
                request.data["author_url"] = sender["id"]
                Likes.objects.create(**request.data)

                # Create Notification
                # notification = Notification(type="Like", author=author, actor=sender["id"], summary=request.data["summary"])
                # notification.save()

                # Return Response
                return Response({"success": "Like Delivered!"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid Like Object Received!"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data["type"].lower() == "comment":
            if "post" in request.data and "author" in request.data and "url" in request.data["author"] and "displayName" in request.data["author"]:
                hosts = [node.host.split("//")[1].rstrip("/").rstrip("/api") for node in Node.objects.all()]
                if [host in request.data["author"]["url"] for host in hosts].count(True) > 0:
                    comment_author = helpers.get(request.data["author"]["url"])
                    if comment_author.status_code == 200:
                        # Save New Comment
                        post: Post = get_object_or_404(Post, local_id=request.data["post"].split("/posts/")[-1].rstrip("/"))
                        comment = Comment(author_url=request.data["author"]["url"], comment=request.data["comment"], contentType=request.data.get("contentType", Post.ContentType.PLAIN_TEXT), post=post)
                        comment.save()

                        # Save Notification
                        summary = f"{request.data['author']['displayName']} Commented On Your Post!"
                        notification = Notification(type="Comment", author=author, actor=request.data["author"]["url"], summary=summary)
                        notification.save()

                        # Create Response
                        response = CommentSerializer(comment).data
                        response["author"] = comment_author.json()
                        return Response(response, status=status.HTTP_201_CREATED)
                    return Response({"error": "Comment Author Not Found!"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"error": "Comment Author Not From Recognized Host!"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Invalid Comment Object Received!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid Type: Must Be One Of 'post', 'follow', 'comment', Or 'like'!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(Author, local_id=kwargs["author"])
        if request.user.author.local_id == author.local_id or not request.user.is_staff:
            InboxItem.objects.filter(owner__local_id=author.local_id).delete()
            return Response({"success": f"Deleted Inbox For {author.displayName}"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "You Are Not Authorized To Delete This Inbox!"}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        author = self.kwargs["author"]
        return InboxItem.objects.filter(owner__local_id=author).order_by("-published")

    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            permission_classes = [IsAuthenticated, IsInboxOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
