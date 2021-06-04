from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client, RequestFactory, testcases

import graphene
from graphene_django.settings import graphene_settings

from .views import GraphQLView


class SchemaRequestFactory(RequestFactory):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self._schema = graphene_settings.SCHEMA

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)

    def execute(self, query, **options):
        return self._schema.execute(query, **options)


class SchemaClient(SchemaRequestFactory, Client):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self._credentials = {}
        self._user = AnonymousUser()

    def request(self, **request):
        request = WSGIRequest(self._base_environ(**request))
        request.user = self._user
        return request

    def authenticate(self, user):
        self._user = user

    def execute(self, query, variables=None, **extra):
        extra.update(self._credentials)
        context = self.post('/', **extra)

        result = super().execute(
            query,
            context_value=context,
            variable_values=variables,
        )
        if result.errors is not None:
            result.errors = [
                GraphQLView.format_error(error)
                for error in result.errors
            ]
        return result


class SchemaTestCase(testcases.TestCase):
    client_class = SchemaClient

    def execute(self, query, variables=None, **extra):
        return self.client.execute(query, variables, **extra)
