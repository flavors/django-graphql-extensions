from django.contrib.auth import get_user_model

from graphql_extensions.test import SchemaTestCase

from . import schema

UserModel = get_user_model()


class SchemaTestCaseTests(SchemaTestCase):

    def setUp(self):
        self.client.schema(query=schema.Query)
        self.user = UserModel.objects.create_user(username='test')

    def test_viewer(self):
        query = '''
        {
            viewer {
                username
            }
        }
        '''

        result = self.client.execute(query=query)
        self.assertTrue(result.errors)

        self.client.authenticate(self.user)

        result = self.client.execute(query=query)
        data = result.data['viewer']

        self.assertFalse(result.errors)
        self.assertEqual(data['username'], self.user.username)
