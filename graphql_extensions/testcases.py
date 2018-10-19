from django.contrib.auth import get_user
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client, RequestFactory, testcases

import graphene
from graphene_django.settings import graphene_settings

from .views import GraphQLView


class SchemaRequestFactory(RequestFactory):

    def execute(self, context, query, variables):
        response = self._schema.execute(
            query,
            context=context,
            variables=variables)

        if response.errors is not None:
            response.errors = [
                GraphQLView.format_error(error)
                for error in response.errors
            ]

        return response


class SchemaClient(SchemaRequestFactory, Client):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self._schema = graphene_settings.SCHEMA

    def request(self, **request):
        request = WSGIRequest(self._base_environ(**request))

        if self.session:
            request.session = self.session
            request.user = get_user(request)
        return request

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)

    def execute(self, query, variables=None, **headers):
        context = self.post('/', **headers)
        return super().execute(context, query, variables)


class SchemaTestCase(testcases.TestCase):
    client_class = SchemaClient
