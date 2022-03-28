from backend.helpers import get
from rest_framework import serializers
from comment.models import Comment
from likes.models import Likes


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    likeCount = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        write_only_fields = ["local_id", "post"]
        read_only_fields = ["author"]
        fields = ["type", "author", "comment", "contentType", "published", "id", "likeCount"]

    def get_author(self, obj: Comment):
        return obj.author_url

    def get_likeCount(self, obj: Comment):
        likes = Likes.objects.filter(object__contains=obj.id)
        return len(likes)
