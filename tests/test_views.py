from django.test import TestCase

from graphql_extensions.views import GraphQLView


class ViewsTests(TestCase):

    def test_format_error(self):
        error = ValueError()
        formatted_error = GraphQLView.format_error(error)
        self.assertEqual(formatted_error['code'], 'error')
