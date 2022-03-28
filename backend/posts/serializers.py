from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorSerializer
from likes.models import Likes


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    likeCount = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["type", "title", "id", "source", "origin", "description", "comments", "contentType", "content", "author", "categories", "published", "visibility", "unlisted", "likeCount"]

    def get_comments(self, obj: Post):
        return f"{obj.id}/comments/"

    def get_likeCount(self, obj: Post):
        likes = Likes.objects.filter(object__contains=obj.id)
        return len(likes)
