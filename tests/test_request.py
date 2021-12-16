import pytest
from django.test import TestCase
from graphene.test import Client

from django_psql.schema import schema
import requests


query1 = """
	query{
	    request(token:"qwertyuiop")
	}
"""
query2 = """
	query{
	    request(token:"qertuiop")
	}
"""


@pytest.mark.django_db
class TestRequest(TestCase):

	def setup(self):
		self.client = Client(schema)


	def test_get_request(self):
		url = "http://127.0.0.1:8000/"

		response = requests.get(url=url, json={'query': query1})

		assert response.status_code == 200

	def test_invalid_token(self):
		url = "http://127.0.0.1:8000/"

		response = requests.get(url=url, json={'query': query2})	
		if "errors" in response.json():
			message = response.json()['errors'][0].get('message')

		assert message == "Invalid token"

