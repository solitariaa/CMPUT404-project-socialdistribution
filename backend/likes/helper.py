import json
from backend.helpers import get_author_list
from likes.serializers import LikesSerializer, LikedSerializer


def get_likes_helper(likes):
    authors = get_author_list([like["author"] for like in likes])
    for like in likes:
        found = False
        for author in authors:
            if "id" in author and (author["id"].split("/authors/")[-1].rstrip("/") == like["author"].split("/authors/")[-1].rstrip("/")):
                found = True
                like["author"] = author
                break
        if not found:
            like["author"] = {"error": "Author Not Found!"}
    return likes


def get_likes(like_objects):
    return {"type": "likes", "items": get_likes_helper(json.loads(json.dumps(LikesSerializer(like_objects, many=True).data)))}
