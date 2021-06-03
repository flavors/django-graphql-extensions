from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.test import RequestFactory, TestCase

from graphql_extensions import decorators, exceptions


class DecoratorTestCase(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='test',
            password='dolphins',
        )

    def info(self, user=None, **headers):
        request = self.request_factory.post('/', **headers)

        if user is not None:
            request.user = user

        return mock.Mock(
            context=request,
            path=['test'],
        )


class UserPassesTests(DecoratorTestCase):

    def test_user_passes_test(self):
        result = decorators.user_passes_test(
            lambda u: u.pk == self.user.pk,
        )(lambda info: None)(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.user_passes_test(
            lambda u: u.pk == self.user.pk + 1,
        )(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(self.user))


class LoginRequiredTests(DecoratorTestCase):

    def test_login_required(self):
        result = decorators.login_required(
            lambda info: None,
        )(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.login_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(AnonymousUser()))


class StaffMemberRequiredTests(DecoratorTestCase):

    def test_staff_member_required(self):
        self.user.is_staff = True

        result = decorators.staff_member_required(
            lambda info: None,
        )(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.staff_member_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(self.user))


class SuperuserRequiredTests(DecoratorTestCase):

    def test_superuser_required(self):
        self.user.is_superuser = True

        result = decorators.superuser_required(
            lambda info: None,
        )(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.superuser_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(self.user))


class PermissionRequiredTests(DecoratorTestCase):

    def test_permission_required(self):
        perm = Permission.objects.get(codename='add_user')
        self.user.user_permissions.add(perm)

        result = decorators.permission_required('auth.add_user')(
            lambda info: None,
        )(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.permission_required(
            ['auth.add_user', 'auth.change_user'],
        )(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(self.user))
