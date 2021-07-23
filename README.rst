Django GraphQL Extensions
=========================

|Pypi| |Build Status| |Codecov| |Codacy|

A collection of custom extensions for `Django GraphQL`_

.. _Django GraphQL: https://github.com/graphql-python/graphene-django


Dependencies
------------

* Python ≥ 3.6
* Django ≥ 2.0
* Graphene-django ≥ 3.0.0b1


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-extensions


Authentication
--------------

- ``@login_required``
- ``@staff_member_required``
- ``@superuser_required``
- ``@permission_required``
- ``@user_passes_test``

See the `documentation`_ to know the full list of decorators.

.. _documentation: https://github.com/flavors/django-graphql-extensions/wiki/Decorators

.. code:: python

    from django.contrib.auth import get_user_model

    import graphene
    from graphql_extensions.decorators import (
        login_required, staff_member_required,
    )


    class Query(graphene.ObjectType):
        viewer = graphene.Field(UserType)
        users = graphene.List(UserType)

        @login_required
        def resolve_viewer(self, info, **kwargs):
            return info.context.user

        @staff_member_required
        def resolve_users(self, info, **kwargs):
            return get_user_model().objects.all()


Errors
------

Returning appropriate **error responses** and **masking** error messages sent to the client.

Configure your ``GraphQLView``.

.. code:: python

    from django.urls import include, path

    from graphql_extensions.views import GraphQLView

    urlpatterns = [
        path('', GraphQLView.as_view(), name='index'),
    ]

**Exceptions**

.. code:: python

    from graphql_extensions import exceptions


- ``exceptions.GraphQLError``
- ``exceptions.PermissionDenied``
- ``exceptions.ValidationError``
- ``exceptions.NotFound``


**Payload**

.. code:: js

    {
      "errors": [
        {
          "message": "You do not have permission to perform this action",
          "locations": [
            {
              "line": 3,
              "column": 13
            }
          ],
          "path": [
            "viewer"
          ],
          "extensions": {
            "type": "PermissionDenied",
            "code": "permissionDenied",
            "timestamp": 1622783872,
            "data": {},
            "operation": "QUERY",
            "trace": [
              "  File \"site-packages/graphql/execution/execute.py\", line 617, in resolve_field\n    result = resolve_fn(source, info, **args)\n",
              "  File \"graphql_extensions/decorators.py\", line 23, in wrapper\n    return func(info.context, *args, **kwargs)\n",
              "  File \"graphql_extensions/decorators.py\", line 35, in wrapper\n    raise exc\n"
            ]
          }
        }
      ],
      "data": {
        "viewer": null
      }
    }


Writing tests
-------------

This package includes a subclass of `unittest.TestCase <https://docs.python.org/3/library/unittest.html#unittest.TestCase>`__ ``SchemaTestCase`` and improve support for making GraphQL queries.

.. code:: python

    from django.contrib.auth import get_user_model

    from graphql_extensions.test import SchemaTestCase


    class UsersTests(SchemaTestCase):

        def test_create_user(self):
            query = '''
            mutation CreateUser($username: String!, $password: String!) {
              createUser(username: $username, password: $password) {
                user {
                  id
                }
              }
            }'''

            response = self.client.execute(query, {
                'username': 'test',
                'password': 'dolphins',
            })

            self.assertFalse(response.errors)
            self.assertTrue(response.data['user'])

        def test_viewer(self):
            user = get_user_model().objects.create_user(
                username='test',
                password='dolphins',
            )

            self.client.authenticate(self.user)

            query = '''
            {
              viewer {
                username
              }
            }'''

            response = self.client.execute(query)
            data = response.data['viewer']

            self.assertEqual(data['username'], user.username)


Types
-----

Custom *Graphene* **types**.

- ``Email``
- ``Timestamp``


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-extensions.svg
   :target: https://pypi.python.org/pypi/django-graphql-extensions
   :alt: Pypi

.. |Build Status| image:: https://github.com/flavors/django-graphql-extensions/actions/workflows/test-suite.yml/badge.svg
   :target: https://github.com/flavors/django-graphql-extensions/actions
   :alt: Build Status

.. |Codecov| image:: https://codecov.io/gh/flavors/django-graphql-extensions/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/flavors/django-graphql-extensions
   :alt: Codecov

.. |Codacy| image:: https://app.codacy.com/project/badge/Grade/95cb35fad84c4560973181a22352ac4b
   :target: https://www.codacy.com/gh/flavors/django-graphql-extensions/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=flavors/django-graphql-extensions&amp;utm_campaign=Badge_Grade
   :alt: Codacy
