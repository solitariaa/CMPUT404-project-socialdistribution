from rest_framework import serializers
from comment.models import Comment
from comment.serializers import CommentSerializer
from .models import Post
from authors.serializers import AuthorSerializer
from likes.models import Likes
from comment.helpers import get_comments


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    likeCount = serializers.SerializerMethodField()
    commentsSrc = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["type", "title", "id", "source", "origin", "description", "comments", "contentType", "content", "author", "categories", "published", "visibility", "unlisted", "likeCount", "commentsSrc"]

    def get_commentsSrc(self, obj: Post):
        # print(CommentViewSet.as_view({"get": "list"})(post=obj.local_id, author=obj.author.local_id))
        comments = obj.comment_set.all()
        comments = get_comments(comments)
        return {"type": "comments",
                "post": obj.id,
                "id": f"{obj.id.rstrip('/')}/comments/",
                "comments": comments}

    def get_comments(self, obj: Post):
        return f"{obj.id}/comments/"

    def get_likeCount(self, obj: Post):
        likes = Likes.objects.filter(object=obj.id)
        return len(likes)
