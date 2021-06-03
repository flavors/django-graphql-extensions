from django.contrib.auth import get_user_model
from django.test import testcases

from graphql_extensions import test

from . import schema


class TestCase(testcases.TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='dolphins',
        )


class SchemaTestCase(TestCase, test.SchemaTestCase):
    Query = schema.Query
    Mutations = None

    def setUp(self):
        super().setUp()
        self.client.schema(query=self.Query)
