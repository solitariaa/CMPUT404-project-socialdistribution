import json

from django import db
from concurrent.futures import ThreadPoolExecutor
from authors.models import Author
from authors.serializers import AuthorSerializer
from urllib import parse
from nodes.models import Node
from requests.auth import HTTPBasicAuth
import requests as r
from django.conf import settings


def get_node(url):
    nodes = Node.objects.filter(host__contains=parse.urlparse(url).hostname)
    return nodes[0] if len(nodes) > 0 else None


def prepare_request(url, headers):
    node: Node = get_node(url)
    auth = None
    if node is None:
        print(url, node, parse.urlparse(url).hostname)
    if node is not None and (settings.DOMAIN not in node.host or headers is None or "Authorization" not in headers):
        auth = HTTPBasicAuth(username=node.outbound_username, password=node.outbound_password)
    if node is not None and settings.DOMAIN not in node.host and headers is not None:
        headers.pop("Authorization")
    if node is not None and (node.host in "http://squawker-cmput404.herokuapp.com/api/" or node.host in "https://squawker-cmput404.herokuapp.com/api/"):
        if "/api/" not in url:
            url = "http://squawker-cmput404.herokuapp.com/api" + url.split("squawker-cmput404.herokuapp.com")[1]
        url = url.rstrip("/")
    if node is not None and ("c404-social-distribution.herokuapp.com" in url) and ("follow" not in url):
        url = "http://c404-social-distribution.herokuapp.com/service" + url.split("c404-social-distribution.herokuapp.com")[1]
        url = url.rstrip("/")
    return url, auth, headers


def get(url, headers=None, params=None):
    url, auth, headers = prepare_request(url, headers)
    res = r.get(url, headers=headers, params=params, auth=auth)
    return res


def post(url, data, headers=None):
    url, auth, headers = prepare_request(url, headers)
    res = r.post(url, data=data, headers=headers, auth=auth)
    return res


def delete(url, headers=None):
    url, auth, headers = prepare_request(url, headers)
    return r.delete(url, headers=headers, auth=auth)


def patch(url, data, headers=None):
    url, auth, headers = prepare_request(url, headers)
    return r.patch(url, data=data, headers=headers, auth=auth)


def put(url, data, headers=None):
    url, auth, headers = prepare_request(url, headers)
    res = r.put(url, data=data, headers=headers, auth=auth)
    print(url, res.status_code)
    return res


def get_author(author, headers=None):
    node = get_node(author)
    if node is None:
        return {"error": "Author Not Found!"}
    if node.host.rstrip("/") in settings.DOMAIN:
        authors = Author.objects.filter(id__contains=author)
        return AuthorSerializer(authors[0]).data if len(authors) > 0 else {"error": "Author Not Found!"}
    response = get(author, headers)
    return response.json() if response is not None and response.status_code == 200 else {"error": "Author Not Found!"}


def get_author_list(authors, headers=None):
    # Fetch Local Authors
    local_authors = [get_author(author) for author in authors if get_hostname(author) in settings.DOMAIN]

    # Fetch Remote Authors
    remote_authors = [author for author in authors if get_hostname(author) not in settings.DOMAIN]
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.map(lambda author: get_author(author), remote_authors)

    # Sort And Return Authors
    return local_authors + [author for author in future]


def get_authors(host: str, headers=None):
    response = get(f"{host.rstrip('/')}/authors/", headers)
    # print(host, response.status_code)
    return response.json() if response is not None and response.status_code == 200 else {"error": "Cannot Connect To Host!"}


def get_likes(object_with_likes: str):
    node = get_node(object_with_likes)
    if node is not None:
        response = get(f"{object_with_likes.rstrip('/')}/likes/")
        if response.status_code == 200:
            contents = response.json()
            if "items" in contents:
                return contents["items"]
            elif "likes" in contents:
                return contents["likes"]
            return []
        return []
    return []


def get_hostname(url):
    if parse.urlparse(url).hostname is None:
        return ""
    return parse.urlparse(url).hostname


def extract_local_id(author):
    return author["id"].split("/authors/")[1].rstrip("/")


def extract_inbox_url(author):
    host = author["host"]
    if host.rstrip("/") in "http://squawker-cmput404.herokuapp.com/" or host.rstrip("/") in "https://squawker-cmput404.herokuapp.com/":
        return f"{host}api/authors/{extract_local_id(author)}/inbox"
    return f"{host}api/authors/{extract_local_id(author)}/inbox/"


def extract_profile_image(author):
    return author["profileImage"] if ("http://" in author["profileImage"] or "https://" in author["profileImage"]) else "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png"


def extract_visibility(remote_post):
    return remote_post["visibility"].upper() if remote_post["visibility"].lower() == "public" or remote_post["visibility"].lower() == "friends" else remote_post["visibility"]


def extract_remote_id(url):
    host = get_hostname(url)
    if host.rstrip("/") in "http://squawker-cmput404.herokuapp.com/" or host.rstrip("/") in "https://squawker-cmput404.herokuapp.com/":
        return f"http://{host}/api/authors/{url.split('/authors/')[1]}"
    return url


def extract_content_type(remote_post):
    if "content_type" in remote_post:
        return remote_post["content_type"]
    return remote_post["contentType"]


def extract_posts_url(author):
    host = author["host"]
    if host.rstrip("/") in "http://squawker-cmput404.herokuapp.com/" or host.rstrip("/") in "https://squawker-cmput404.herokuapp.com/":
        return f"{host}api/authors/{extract_local_id(author)}/posts"
    return f"{host}authors/{extract_local_id(author)}/posts/"


def extract_likes(object_with_likes):
    host = get_hostname(object_with_likes["id"])
    if host.rstrip("/") in "http://squawker-cmput404.herokuapp.com/" or host.rstrip("/") in "https://squawker-cmput404.herokuapp.com/":
        return object_with_likes["num_likes"]
    return object_with_likes["likeCount"] if "likeCount" in object_with_likes else 0


def validate_author(author):
    author["id"] = extract_remote_id(author["id"])
    author["url"] = author["id"]
    author["profileImage"] = extract_profile_image(author)
    return author


def validate_post(post):
    post["visibility"] = extract_visibility(post)
    post["id"] = extract_remote_id(post["id"])
    post["url"] = extract_remote_id(post["id"])
    post["contentType"] = extract_content_type(post)
    post["author"] = validate_author(post["author"])
    post["likeCount"] = extract_likes(post)
    return post


def validate_comment(comment):
    comment["likeCount"] = extract_likes(comment)
    comment["id"] = extract_remote_id(comment["id"])
    comment["url"] = extract_remote_id(comment["id"])
    comment["contentType"] = extract_content_type(comment)
    comment["author"] = validate_author(comment["author"])
    return comment


def validate_proxy(res):
    if type(res) == bytes:
        res = json.loads(res.decode('utf-8'))
    if "type" in res and "comment" == res["type"].lower():
        return validate_comment(res)
    elif "type" in res and "comments" == res["type"].lower() and "comments" in res:
        res["comments"] = [validate_comment(comment) for comment in res["comments"]]
        return res
    elif "type" in res and "comments" == res["type"].lower() and "items" in res:
        res["comments"] = [validate_comment(comment) for comment in res["items"]]
        return res
    elif "type" in res and "post" == res["type"].lower():
        return validate_post(res)
    return res
