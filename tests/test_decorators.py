from unittest.mock import Mock

from django.contrib.auth import models
from django.test import RequestFactory

from graphql_extensions import decorators, exceptions

from .testcases import TestCase


class DecoratorsTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.request_factory = RequestFactory()

    def info(self, user, **kwargs):
        request = self.request_factory.post('/', **kwargs)
        request.user = user
        return Mock(context=request)


class UserPassesTests(DecoratorsTestCase):

    def test_user_passes_test(self):

        @decorators.user_passes_test(lambda u: u.pk == self.user.pk)
        def wrapped(info):
            """Decorated function"""

        result = wrapped(self.info(self.user))
        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.user_passes_test(lambda u: u.pk == self.user.pk + 1)
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(self.user))


class LoginRequiredTests(DecoratorsTestCase):

    def test_login_required(self):

        @decorators.login_required
        def wrapped(info):
            """Decorated function"""

        result = wrapped(self.info(self.user))
        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.login_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(models.AnonymousUser()))


class StaffMemberRequiredTests(DecoratorsTestCase):

    def test_staff_member_required(self):

        @decorators.staff_member_required
        def wrapped(info):
            """Decorated function"""

        self.user.is_staff = True
        result = wrapped(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.staff_member_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(self.user))


class PermissionRequiredTests(DecoratorsTestCase):

    def test_permission_required(self):

        @decorators.permission_required('auth.add_user')
        def wrapped(info):
            """Decorated function"""

        perm = models.Permission.objects.get(codename='add_user')
        self.user.user_permissions.add(perm)

        result = wrapped(self.info(self.user))
        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.permission_required(['auth.add_user', 'auth.change_user'])
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(self.user))
