from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import testcases

from graphql_extensions import testcases as extensions_testcases

from . import schema


class TestCase(testcases.TestCase):

    def setUp(self):
        self.group = Group.objects.create(name='flavors')
        self.user = get_user_model().objects.create_user(
            username='test',
            password='dolphins')


class SchemaTestCase(TestCase, extensions_testcases.SchemaTestCase):
    Query = schema.Query
    Mutations = None

    def setUp(self):
        super().setUp()
        self.client.schema(query=self.Query, mutation=self.Mutations)
