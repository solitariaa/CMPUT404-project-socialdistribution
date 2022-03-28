from rest_framework.parsers import JSONParser
from likes.models import Likes
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .models import InboxItem
from notifications.models import Notification
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

        # Fetch Queryset
        queryset = self.get_queryset()

        # Check Object Permissions
        for q in queryset:
            self.check_object_permissions(request, q)

        # Fetch Local Posts
        local_posts_src = [item.src for item in queryset if item.src.split("/authors/")[0] == settings.DOMAIN]
        print("asdasdasdasd")
        local_posts = [PostSerializer(p).data for p in Post.objects.filter(id__in=local_posts_src) if not p.unlisted]
        print(local_posts)

        # Fetch Foreign Posts
        # with ThreadPoolExecutor(max_workers=1) as executor:
        #   future = executor.map(lambda x: x.get_post(), [item for item in queryset if item.src.split("/authors/")[0] != settings.DOMAIN])
        # foreign_posts = [p for p in future if "unlisted" in p and not p["unlisted"]]

        # Get List Of Remote Authors
        authors = []
        nodes = Node.objects.all()
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = executor.map(lambda node: helpers.get_authors(node), [node.host for node in nodes if node.host.rstrip("/") not in settings.DOMAIN.rstrip("/")])
        for future in futures:
            if "items" in future:
                authors += future["items"]

        # Get Posts From Remote Authors
        urls = [helpers.extract_posts_url(author) for author in authors]
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = executor.map(lambda url: helpers.get(url), urls)

        # Prepare Fetched Remote Posts
        foreign_posts = []
        for f in futures:
            print(f.headers)
            if f is not None and f.status_code == 200 and "application/json" in f.headers.get("Content-Type", ""):
                if "posts" in f.json():
                    foreign_posts += f.json()["posts"]
                elif "items" in f.json():
                    foreign_posts += f.json()["items"]

        # Get Likes On Posts
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = executor.map(lambda p: helpers.validate_post(p), foreign_posts)
        foreign_posts = [f for f in futures]

        # Paginate Response
        posts = local_posts + foreign_posts
        posts.sort(key=lambda x: x.get("published", '2022-03-24T18:22:07.990808-06:00'), reverse=True)
        posts = list(filter(lambda x: "image" not in x["contentType"], posts))
        page = self.paginator.paginate_queryset(posts, request)

        # Return Response
        return self.paginator.get_paginated_response(page, author=owner.local_id)

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        author = get_object_or_404(Author, local_id=kwargs["author"])
        if request.data["type"].lower() == "post":
            if request.data["author"]["host"].rstrip("/") == settings.DOMAIN.rstrip("/") or request.data["visibility"].lower() != "public":
                inbox_item = InboxItem(owner=author, src=request.data["id"])
                inbox_item.save()
                return Response(InboxItemSerializer(inbox_item).data, status=status.HTTP_201_CREATED)
            return Response({"ok": "Successfully Posted To Inbox!"}, status=status.HTTP_200_OK)
        elif request.data["type"].lower() == "follow":
            summary = f"{request.data['actor']['displayName']} Wants To Follow You!"
            notification = Notification(type="Follow", author=author, actor=request.data["actor"]["url"], summary=summary)
            notification.save()
            return Response({"success": "Follow Request Delivered!"}, status=status.HTTP_200_OK)
        elif request.data["type"].lower() == "like":
            notification = Notification(type="Like", author=author, actor=request.data["author"]["url"], summary=request.data["summary"])
            notification.save()
            request.data.pop("@context", "")
            like_author = request.data.pop("author")
            like = Likes.objects.create(**request.data)
            like.author_url = like_author["id"]
            like.save()
            return Response({"success": "Like Delivered!"}, status=status.HTTP_200_OK)
        elif request.data["type"].lower() == "comment":
            summary = f"{request.data['author']['displayName']} Commented On Your Post!"
            notification = Notification(type="Comment", author=author, actor=request.data["author"]["url"], summary=summary)
            notification.save()
            return Response({"success": "Comment Delivered!"}, status=status.HTTP_200_OK)
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
