from django.test import TestCase, override_settings

from graphql.error import GraphQLError

from graphql_extensions.views import GraphQLView


class ViewsTests(TestCase):

    @override_settings(DEBUG=True)
    def test_format_error(self):
        try:
            raise RuntimeError
        except RuntimeError as e:
            formatted = GraphQLView.format_error(
                GraphQLError('', original_error=e),
            )

        extensions = formatted['extensions']

        self.assertEqual(extensions['type'], 'RuntimeError')
        self.assertEqual(extensions['code'], 'error')
        self.assertIsInstance(extensions['timestamp'], int)
        self.assertTrue(extensions['trace'])
