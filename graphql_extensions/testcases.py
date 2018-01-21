from django.contrib.auth import get_user
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client, RequestFactory, testcases

from graphene_django.settings import graphene_settings

from .views import GraphQLView


class GraphQLRequestFactory(RequestFactory):

    def execute(self, context, query, variables, extra):
        response = self._schema.execute(
            query,
            context_value=context,
            variable_values=variables)

        if response.errors is not None:
            response.errors = [
                GraphQLView.format_error(error)
                for error in response.errors
            ]

        return response


class GraphQLClient(GraphQLRequestFactory, Client):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self._credentials = {}
        self._schema = graphene_settings.SCHEMA

    def request(self, **request):
        request = WSGIRequest(self._base_environ(**request))

        if self.session:
            request.session = self.session
            request.user = get_user(request)
        return request

    def credentials(self, **kwargs):
        self._credentials = kwargs

    def execute(self, query, variables=None, **extra):
        extra.update(self._credentials)
        context = self.post('/', **extra)
        return super().execute(context, query, variables, extra)

    def logout(self):
        super().logout()
        self._credentials.pop('HTTP_AUTHORIZATION', None)


class GraphQLTestCase(testcases.TestCase):
    client_class = GraphQLClient
