from datetime import datetime

from django.test import TestCase

from graphql.language import ast

from graphql_extensions import exceptions, types


class TimestampTests(TestCase):

    def test_timestamp(self):
        now = datetime.now()
        node = ast.IntValueNode(value=now.timestamp())
        serialized = types.Timestamp.serialize(now)
        parsed = types.Timestamp.parse_literal(node)

        self.assertEqual(serialized, int(now.timestamp()))
        self.assertEqual(parsed, now)


class EmailTests(TestCase):

    def test_email(self):
        email = 'a@b.cd'
        node = ast.StringValueNode(value=email)
        serialized = types.Email.serialize(email)
        parsed = types.Email.parse_literal(node)

        self.assertEqual(serialized, email)
        self.assertEqual(parsed, email)

        with self.assertRaises(exceptions.ValidationError):
            types.Email().parse_value('invalid')
