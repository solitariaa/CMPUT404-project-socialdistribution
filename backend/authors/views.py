import base64
from nodes.models import Node
from concurrent.futures import ThreadPoolExecutor
from backend import helpers
from django.conf import settings
from functools import reduce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.decorators import action
from django.db.utils import IntegrityError
from .models import Author, Avatar
from django.contrib.auth.models import User
from .serializers import AuthorSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib import auth
from rest_framework.authtoken.models import Token
from likes.models import Liked
from likes.serializers import LikedSerializer
from .helpers import get_all_authors


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({'type': "authors", 'items': data})


class AuthorViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AuthorSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        nodes = Node.objects.all()
        node_users = [node.username for node in nodes]
        return Author.objects.all().exclude(displayName__in=node_users).order_by("displayName")

    def list(self, request, *args, **kwargs):
        all_authors = request.query_params.get("remote", "false")
        authors = get_all_authors(all_authors == "true")
        page = self.paginator.paginate_queryset(authors, request)
        return self.paginator.get_paginated_response(page)

    @action(detail=True, methods=['GET', "POST"])
    def liked(self, request, pk):
        if request.method == "GET":
            author: Author = get_object_or_404(Author, local_id=pk)
            liked = author.liked_set.all()
            return Response({"type": "liked", "items": LikedSerializer(liked, many=True).data}, content_type="application/json")
        request.data.pop("@context", "")
        author = get_object_or_404(Author, local_id=pk)
        request.data["author"] = author
        like = Liked.objects.create(**request.data)
        response = LikedSerializer(like).data
        response["author"] = AuthorSerializer(author).data
        return Response(response, content_type="application/json")

    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            user = User.objects.create_user(username=request.data["displayName"], password=request.data["password"])
            author = user.author
            author.github = "https://www.github.com/" + request.data["github"]
            author.save()
            return Response(AuthorSerializer(author).data)
        except IntegrityError:
            return Response({"error": "Username Already Exists!"}, status=status.HTTP_409_CONFLICT)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        user = auth.authenticate(username=request.data["displayName"], password=request.data["password"])
        if user is not None:
            author = user.author
            if author.verified:
                auth.login(request, user)
                response = {'message': 'Successfully Logged In!', 'author': AuthorSerializer(author).data, 'token': Token.objects.get_or_create(user=user)[0].key }
                return Response(response, status=status.HTTP_200_OK)
            return Response({"error": "Your Account Is Awaiting Approval By The Admin!"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Invalid Username Or Password!"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        user: User = request.user
        user.auth_token.delete()
        return Response({"message": "Succesfully Logged Out!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET', 'PATCH'])
    def avatar(self, request, pk):
        author: Author = get_object_or_404(Author, local_id=pk)
        avatar: Avatar = author.avatar
        if request.method == "GET":
            string = avatar.content
            content = string.split("base64,")[1]
            mimetype = string.split(";base64,")[0].split(":")[1]
            response = HttpResponse(content_type=mimetype)
            response.write(base64.b64decode(content))
            return response
        avatar.content = request.data["content"]
        avatar.save()
        return Response({"ok": "Successfully Changed Avatar!"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
