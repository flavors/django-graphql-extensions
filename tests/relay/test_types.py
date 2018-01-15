import random

from django.test import TestCase

from graphql.language import ast
from graphql_relay import to_global_id

from graphql_extensions import exceptions
from graphql_extensions.relay import types


class GraphQLTypesTests(TestCase):

    def test_global_id(self):
        global_id_type = types.GlobalID()
        random_id = random.randint(1, 10 ** 10)
        global_id = to_global_id('Test', random_id)
        node = ast.StringValue(global_id)

        self.assertEqual(global_id_type.serialize(global_id), global_id)
        self.assertEqual(global_id_type.parse_literal(node), random_id)

    def test_global_id_error(self):
        global_id_type = types.GlobalID()
        node = ast.StringValue('invalid')

        with self.assertRaises(exceptions.ValidationError):
            global_id_type.parse_literal(node)
