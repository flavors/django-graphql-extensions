from django.test import TestCase

from graphql_extensions import utils


class UtilsTests(TestCase):

    def test_to_camel(self):
        camel = utils.dashed_to_camel({
            'a_b': {
                'a_c': True,
            },
        })

        self.assertTrue(camel['aB']['aC'])
