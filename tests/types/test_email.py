from django.test import TestCase

from graphql.language import ast

from graphql_extensions import exceptions, types


class EmailTypeTests(TestCase):

    def test_email(self):
        email = 'do@make.test'
        email_type = types.Email()
        node = ast.StringValue(email)

        self.assertEqual(email_type.serialize(email), email)
        self.assertEqual(email_type.parse_literal(node), email)

        with self.assertRaises(exceptions.ValidationError):
            email_type.parse_value('invalid')
