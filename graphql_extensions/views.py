import traceback
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _

from graphene_django.views import GraphQLView as BaseGraphQLView
from graphql.error import GraphQLError
from graphql.error import format_error as format_graphql_error
from graphql.error.located_error import GraphQLLocatedError

from . import exceptions
from .settings import extensions_settings


def show_error_message(error):
    return settings.DEBUG or isinstance(error, (
        exceptions.GraphQLError,
        GraphQLError,
    ))


class GraphQLView(BaseGraphQLView):

    @staticmethod
    def format_error(error):
        if isinstance(error, GraphQLLocatedError):
            error = error.original_error

        formatted_error = format_graphql_error(error)
        graphql_error = OrderedDict([('type', error.__class__.__name__)])

        if extensions_settings.EXT_SHOW_ERROR_MESSAGE_HANDLER(error):
            graphql_error['message'] = formatted_error['message']
        else:
            # Internal errors must be masked
            graphql_error['message'] = _('Internal server error')

        if isinstance(error, exceptions.GraphQLError):
            graphql_error['code'] = error.code

            if error.error_data:
                graphql_error['data'] = error.error_data
        else:
            graphql_error['code'] = 'error'

        if 'location' in formatted_error:
            graphql_error['location'] = formatted_error['location']

        if error.__traceback__ is not None:
            info = error.__traceback__.tb_frame.f_locals.get('info')

            if info is not None:
                graphql_error['path'] = [info.field_name]
                graphql_error['operation'] = info.operation.operation

        if settings.DEBUG:
            graphql_error['trace'] = traceback.format_list(
                traceback.extract_tb(error.__traceback__))

        return graphql_error


class LoginRequiredGraphQLView(LoginRequiredMixin, GraphQLView):
    """Adding login required"""
