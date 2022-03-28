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
    p = parse.urlparse(url)
    hostname = f"{p.scheme}://{p.hostname}"
    nodes = Node.objects.filter(host__contains=hostname)
    return nodes[0] if len(nodes) > 0 else None


def prepare_request(url, headers):
    node: Node = get_node(url)
    auth = None
    if node is not None and (settings.DOMAIN not in node.host or headers is None or "Authorization" not in headers):
        auth = HTTPBasicAuth(username=node.outbound_username, password=node.outbound_password)
    if settings.DOMAIN not in node.host and headers is not None:
        headers.pop("Authorization")
    if node.host == "http://squawker-cmput404.herokuapp.com/api/":
        url = url.rstrip("/")
    return url, auth, headers


def get(url, headers=None, params=None):
    url, auth, headers = prepare_request(url, headers)
    res = r.get(url, headers=headers, params=params, auth=auth)
    return res


def post(url, data, headers=None):
    url, auth, headers = prepare_request(url, headers)
    return r.post(url, data=data, headers=headers, auth=auth)


def delete(url, headers=None):
    url, auth, headers = prepare_request(url, headers)
    return r.delete(url, headers=headers, auth=auth)


def patch(url, data, headers=None):
    url, auth, headers = prepare_request(url, headers)
    return r.patch(url, data=data, headers=headers, auth=auth)


def put(url, data, headers=None):
    url, auth, headers = prepare_request(url, headers)
    return r.put(url, data=data, headers=headers, auth=auth)


def get_author(author, headers=None):
    node = get_node(author)
    if node.host.rstrip("/") in settings.DOMAIN:
        authors = Author.objects.filter(id__contains=author)
        return AuthorSerializer(authors[0]).data if len(authors) > 0 else {"error": "Author Not Found!"}
    response = get(author, headers)
    return response.json() if response is not None and response.status_code == 200 else {"error": "Author Not Found!"}


def get_author_list(authors, headers=None):
    # Fetch Local Authors
    local_authors = [get_author(author) for author in authors if get_hostname(author) in settings.DOMAIN]

    # Fetch Remote Authors
    db.connections.close_all()
    remote_authors = [author for author in authors if get_hostname(author) not in settings.DOMAIN]
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.map(lambda author: get_author(author), remote_authors)

    # Sort And Return Authors
    return local_authors + [author for author in future]


def get_authors(host: str, headers=None):
    response = get(f"{host.rstrip('/')}/authors", headers)
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
    p = parse.urlparse(url)
    return f"{p.scheme}://{p.hostname}"


def extract_local_id(author):
    return author["id"].split("/authors/")[1].rstrip("/")


def extract_inbox_url(author):
    host = author["host"]
    if host == "http://squawker-cmput404.herokuapp.com/":
        return f"{host}api/authors/{extract_local_id(author)}/inbox"
    return f"{host}api/authors/{extract_local_id(author)}/inbox/"


def extract_profile_image(author):
    return author["profileImage"] if "http://" in author["profileImage"] else "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png"


def extract_visibility(remote_post):
    host = remote_post["id"]
    if host == "http://squawker-cmput404.herokuapp.com/":
        return remote_post["visibility"].upper() if remote_post["visibility"] == "public" or remote_post["visibility"] == "friends" else remote_post["visibility"]
    return remote_post["visibility"]


def extract_remote_id(url):
    host = get_hostname(url)
    if host.rstrip("/") == "http://squawker-cmput404.herokuapp.com/".rstrip("/"):
        return f"{host}/api/authors/{url.split('/authors/')[1]}"
    return url


def extract_content_type(remote_post):
    host = get_hostname(remote_post["id"])
    if host.rstrip("/") == "http://squawker-cmput404.herokuapp.com/".rstrip("/"):
        return remote_post["content_type"]
    return remote_post["contentType"]


def extract_posts_url(author):
    host = author["host"]
    if host == "http://squawker-cmput404.herokuapp.com/":
        return f"{host}api/authors/{extract_local_id(author)}/posts"
    return f"{host}authors/{extract_local_id(author)}/posts/"


def extract_likes(object_with_likes):
    host = get_hostname(object_with_likes["id"])
    if host == "http://squawker-cmput404.herokuapp.com/":
        return object_with_likes["num_likes"]
    return object_with_likes["likeCount"] if "likeCount" in object_with_likes else 0


def validate_author(author):
    author["id"] = extract_remote_id(author["id"])
    author["url"] = author["url"]
    author["profileImage"] = extract_profile_image(author)
    return author


def validate_post(post):
    post["visibility"] = "PUBLIC"
    post["id"] = extract_remote_id(post["id"])
    post["url"] = extract_remote_id(post["id"])
    post["contentType"] = extract_content_type(post)
    post["author"] = validate_author(post["author"])
    post["likeCount"] = extract_likes(post)
    return post

