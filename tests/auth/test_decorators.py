from unittest.mock import MagicMock, PropertyMock

from django.test import TestCase

from graphql_extensions import exceptions
from graphql_extensions.auth import decorators


class GraphQLDecoratorsTests(TestCase):

    def test_login_required(self):

        @decorators.login_required
        def wrapped(info, *args, **kwargs):
            return True

        info_mock = MagicMock()

        type(info_mock.context.user).is_anonymous =\
            PropertyMock(return_value=False)

        self.assertTrue(wrapped(info_mock))

    def test_login_required_error(self):

        @decorators.login_required
        def wrapped(info, *args, **kwargs):
            """Decorated function"""

        info_mock = MagicMock()

        with self.assertRaises(exceptions.NotAuthenticated):
            wrapped(info_mock)

    def test_staff_member_required(self):

        @decorators.staff_member_required
        def wrapped(info, *args, **kwargs):
            return True

        info_mock = MagicMock()
        self.assertTrue(wrapped(info_mock))

    def test_staff_member_required_error(self):

        @decorators.staff_member_required
        def wrapped(info, *args, **kwargs):
            """Decorated function"""

        info_mock = MagicMock()

        type(info_mock.context.user).is_active =\
            PropertyMock(return_value=False)

        with self.assertRaises(exceptions.NotAuthenticated):
            wrapped(info_mock)
