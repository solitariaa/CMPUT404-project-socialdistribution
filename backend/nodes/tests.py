from django.test import TestCase
from nodes.models import Node
from rest_framework.test import APITestCase
from rest_framework import status
import json


def create_node(name):
    data = {
    "name": name,
    "host": "host",
    "username": f"test_{name}",
    "password": "test_password",
    "outbound_username": f"outbound_{name}",
    "outbound_password": "outboud_test"
    }
    return Node.objects.create(**data)

class NodeTests(APITestCase):

    def test_create_node(self):
        """ Ensure we can create nodes """
        url = "/nodes/"
        data = {"name": "testNode",
        "host": "testHost",
        "username": "test_user",
        "password": "test_password",
        "remote_username": "remote_user",
        "remote_password": "remote_test",
        "outbound_username": "outbound_user",
        "outbound_password": "outboud_test"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "testNode")
        self.assertEqual(response.data["host"], "testHost")
        self.assertEqual(response.data["username"], "test_user")
        self.assertEqual(response.data["password"], "test_password")

    def test_list_nodes(self):
        """ Ensure we can get all nodes """
        node_one = create_node("nodeOne")
        node_two = create_node("nodeTwo")
        url = "/nodes/"
        response = self.client.get(url, format="json")
        data = json.loads(json.dumps(response.data))
        self.assertEqual(data["count"], 2)
        for node in [node_one, node_two]:
            self.assertIn(node.name, map(lambda x: x["name"], data["results"]))
            self.assertIn(node.host, map(lambda x: x["host"], data["results"]))
            self.assertIn(node.username, map(lambda x: x["username"], data["results"]))
            self.assertIn(node.password, map(lambda x: x["password"], data["results"]))