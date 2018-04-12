import datetime

from django.test import TestCase

from graphql.language import ast

from graphql_extensions import types


class TimestampTypeTests(TestCase):

    def test_timestamp(self):
        now = datetime.datetime.now()
        timestamp_type = types.Timestamp()
        node = ast.IntValue(now.timestamp())

        self.assertEqual(timestamp_type.serialize(now), int(now.timestamp()))
        self.assertEqual(timestamp_type.parse_literal(node), now)
