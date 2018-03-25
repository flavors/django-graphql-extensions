from unittest.mock import Mock

from django.contrib.auth import models

from graphql_extensions import exceptions
from graphql_extensions.auth import decorators

from ..testcases import UserTestCase


def info_mock(user):
    return Mock(context=Mock(user=user))


class AuthDecoratorsTests(UserTestCase):

    def test_user_passes_test(self):

        @decorators.user_passes_test(lambda u: u.pk == self.user.pk)
        def wrapped(info):
            """Decorated function"""

        result = wrapped(info_mock(self.user))
        self.assertIsNone(result)

    def test_user_passes_test_permission_denied(self):

        @decorators.user_passes_test(lambda u: u.pk == self.user.pk + 1)
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(info_mock(self.user))

    def test_login_required(self):

        @decorators.login_required
        def wrapped(info):
            """Decorated function"""

        result = wrapped(info_mock(self.user))
        self.assertIsNone(result)

    def test_login_required_permission_denied(self):

        @decorators.login_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(info_mock(models.AnonymousUser()))

    def test_staff_member_required(self):

        @decorators.staff_member_required
        def wrapped(info):
            """Decorated function"""

        self.user.is_staff = True
        result = wrapped(info_mock(self.user))

        self.assertIsNone(result)

    def test_staff_member_required_permission_denied(self):

        @decorators.staff_member_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(info_mock(self.user))

    def test_permission_required(self):

        @decorators.permission_required('auth.add_user')
        def wrapped(info):
            """Decorated function"""

        perm = models.Permission.objects.get(codename='add_user')
        self.user.user_permissions.add(perm)

        result = wrapped(info_mock(self.user))
        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.permission_required(['auth.add_user', 'auth.change_user'])
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(info_mock(self.user))
