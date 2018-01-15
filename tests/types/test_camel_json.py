from django.test import TestCase

from graphql_extensions import types


class CamelJSONTypeTests(TestCase):

    def test_camel_json(self):
        json_type = types.CamelJSON()
        self.assertIn('aB', json_type.serialize({'a_b': None}).keys())
