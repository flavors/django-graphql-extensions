from unittest.mock import MagicMock, PropertyMock

from django.test import TestCase

from graphql_extensions import exceptions
from graphql_extensions.auth import decorators


class GraphQLDecoratorsTests(TestCase):

    def test_login_required_error(self):

        @decorators.login_required
        def wrapped(info, *args, **kwargs):
            return

        info_mock = MagicMock()
        type(info_mock.context.user).is_anonymous =\
            PropertyMock(return_value=True)

        with self.assertRaises(exceptions.NotAuthenticated):
            wrapped(info_mock)
