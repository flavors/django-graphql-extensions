from django.test import TestCase

from graphql_extensions import lookups


class LookupsTypesTests(TestCase):

    def test_lookups(self):
        self.assertTrue(lookups.TEXT_LOOKUPS)
