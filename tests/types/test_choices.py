from django.test import TestCase

from graphql.language import ast

from graphql_extensions import types


class ChoicesTypeTests(TestCase):

    def test_choices(self):
        value = 'test'

        class TestChoices(types.Choices):
            CHOICES = (value,)

        choices_type = TestChoices()
        node = ast.StringValue(value)

        self.assertEqual(choices_type.serialize(value), value)
        self.assertEqual(choices_type.parse_literal(node), value)
