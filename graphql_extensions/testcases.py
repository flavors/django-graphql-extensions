import json

from django.test import Client, RequestFactory, testcases
from django.urls import reverse

from graphene_django.settings import graphene_settings


class GraphQLRequestFactory(RequestFactory):
    default_viewname = 'graphql-index'

    def execute(self, query, variables, viewname=None, **kwargs):
        if viewname is None:
            viewname = self.default_viewname

        response = self.post(
            reverse(viewname), {
                'query': query,
                'variables': json.dumps(variables),
            }, **kwargs)

        data = response.json()
        response.data = data.get('data')
        response.errors = data.get('errors')
        return response


class GraphQLClient(GraphQLRequestFactory, Client):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self._credentials = {}
        self.schema = graphene_settings.SCHEMA

    def credentials(self, **kwargs):
        self._credentials = kwargs

    def execute(self, query, variables=None, **kwargs):
        kwargs.update(self._credentials)
        return super().execute(query, variables, **kwargs)

    def logout(self):
        self._credentials.pop('HTTP_AUTHORIZATION', None)


class GraphQLTestCase(testcases.TestCase):
    client_class = GraphQLClient
