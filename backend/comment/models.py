from django.db import models
import uuid
from authors.models import Author
from posts.models import Post
class Comment(models.Model):
    class ContentType(models.TextChoices):
        COMMON_MARK = "text/markdown"
        PLAIN_TEXT = "text/plain"
        BASE64 = "application/base64"
        PNG = "image/png;base64"
        JPEG = "image/jpeg;base64"    
    type = models.CharField(max_length=100, default="comments")
    comment = models.TextField(blank=False)
    contentType = models.CharField(max_length=350, choices=ContentType.choices)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    local_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, editable=False)
    id = models.CharField(max_length=500, default="post", blank=True)