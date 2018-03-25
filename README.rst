Django GraphQL Extensions
=========================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|

A collection of custom extensions for `Django GraphQL`_

.. _Django GraphQL: https://github.com/graphql-python/graphene-django


Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-extensions


Authentication
--------------

- ``@login_required``
- ``@staff_member_required``
- ``@permission_required``
- ``@user_passes_test``

.. code:: python

    from django.contrib.auth import get_user_model

    import graphene
    from graphql_extensions.auth.decorators import (
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


    raise exceptions.GraphQLError()
    raise exceptions.PermissionDenied()
    raise exceptions.ValidationError()
    raise exceptions.NotFound()


**Payload**

.. code:: js

    {
      "errors": [
        {
          "type": "NotFound",
          "message": "GraphQL object not found",
          "code": "notFound",
          "data": {
            "id": 1
          },
          "path": ["updateGroup"],
          "operation": "mutation",
          "trace": [
            "  File \"/app/schema.py\", line 30, in mutate\n    group = cls.update(info, **kwargs)\n",
            "  File \"/graphql_extensions/mixins.py\", line 32, in update\n    instance = cls.get_object(context, id=id)\n",
            "  File \"/graphql_extensions/mixins.py\", line 21, in get_object\n    raise exceptions.NotFound(**kwargs)\n"
          ]
        }
      ],
      "data": {
        "updateGroup": null
      }
    }


Mixins
------

**Pre-built mutations** that provide for commonly used patterns.

- ``RetrieveMixin``
- ``UpdateMixin``

.. code:: python

    from django.contrib.auth.models import Group

    import graphene
    from graphene_django import DjangoObjectType
    from graphql_extensions import mixins
    from graphql_extensions.auth.decorators import login_required


    class GroupType(DjangoObjectType):

        class Meta:
            model = Group


    class UpdateGroup(mixins.UpdateMixin, graphene.Mutation):
        group = graphene.Field(GroupType)

        class Arguments:
            id = graphene.Int(required=True)
            name = graphene.String()

        @classmethod
        def get_queryset(cls, info, **kwargs):
            return info.context.user.groups.all()

        @classmethod
        @login_required
        def mutate(cls, root, info, **kwargs):
            group = cls.update(info, **kwargs)
            return cls(group=group)


Testing
-------

Helper classes to improve support for **testing**.

- ``GraphQLTestCase``


.. code:: python

    from graphql_extensions.testcases import GraphQLTestCase


    class UsersTests(GraphQLTestCase):

        def test_create_user(self):
            query = '''
            mutation CreateUser($username: String!, $password: String!) {
              createUser(username: $username, password: $password) {
                user {
                  id
                }
              }
            }'''

            username = 'test'
            password = 'dolphins'

            response = self.client.execute(query, {
                'username': username,
                'password': password,
            })

            self.assertFalse(response.errors)
            self.assertTrue(response.data['user'])

            self.client.login(username=username, password=password)

            query = '''
            {
              me {
                username
              }
            }'''

            response = self.client.execute(query)
            self.assertEqual(response.data['me']['username'], username)


Types
-----

Custom *Graphene* **types**.

- ``Email``
- ``Timestamp``
- ``Choices``
- ``CamelJSON``
- ...


Relay
-----

Complete support for `Relay`_.

.. _Relay: https://facebook.github.io/relay/


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-extensions.svg
   :target: https://pypi.python.org/pypi/django-graphql-extensions

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-extensions.svg
   :target: https://pypi.python.org/pypi/django-graphql-extensions

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphql-extensions.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphql-extensions

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphql-extensions.svg
   :target: https://codecov.io/gh/flavors/django-graphql-extensions

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/6ca5da3b6a51d35ea7d6/maintainability
   :target: https://codeclimate.com/github/flavors/django-graphql-extensions
