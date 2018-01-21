from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from graphql_extensions.testcases import GraphQLTestCase


class UserTestcase(GraphQLTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='dolphins')


class GroupTestcase(UserTestcase):

    def setUp(self):
        super().setUp()
        self.group = Group.objects.create(name='flavors')
