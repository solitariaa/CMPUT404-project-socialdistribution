from rest_framework import serializers
from likes.models import Likes, Liked
from authors.serializers import AuthorSerializer


class LikesSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Likes
        fields = ["type", "summary", "context", "object", "author"]

    def get_author(self, obj: Likes):
        return obj.author_url


class LikedSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Liked
        fields = "__all__"
