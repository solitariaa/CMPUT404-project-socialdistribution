from nodes.models import Node
from concurrent.futures import ThreadPoolExecutor
from backend import helpers
from django.conf import settings
from functools import reduce
from .models import Author
from .serializers import AuthorSerializer


def get_all_authors():
    nodes = Node.objects.all()
    node_users = [node.username for node in nodes]
    authors = [AuthorSerializer(author).data for author in Author.objects.all().exclude(displayName__in=node_users).order_by("displayName")]
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = executor.map(lambda node: helpers.get_authors(node), [node.host for node in nodes if node.host.rstrip("/") not in settings.DOMAIN.rstrip("/")])
    remote_authors = reduce(lambda acc, x: acc + (x["items"] if "items" in x else []), futures, [])
    authors += [helpers.validate_author(author) for author in remote_authors]
    authors.sort(key=lambda x: x["displayName"])
    return authors
