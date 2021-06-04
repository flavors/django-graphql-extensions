from django.contrib.auth import get_user_model
from django.test import TestCase

from graphql_extensions import exceptions
from graphql_extensions.shortcuts import get_object_or_not_found


class ShortcutsTests(TestCase):

    def test_get_object_or_not_found(self):
        with self.assertRaises(exceptions.NotFound):
            get_object_or_not_found(get_user_model(), pk=1)
