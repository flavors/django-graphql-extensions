import traceback
from calendar import timegm
from collections import OrderedDict
from datetime import datetime

from django.conf import settings
from django.utils.translation import gettext as _

from graphene_django.views import GraphQLView as BaseGraphQLView
from graphql.error import GraphQLError

from . import exceptions
from .settings import extensions_settings


def show_error_message(error):
    return settings.DEBUG or isinstance(error, (
        GraphQLError,
        exceptions.GraphQLError,
    ))


class GraphQLView(BaseGraphQLView):

    @staticmethod
    def format_error(error):
        formatted = BaseGraphQLView.format_error(error)

        if isinstance(error, GraphQLError) and\
                error.original_error is not None:

            error = error.original_error

        if not extensions_settings.SHOW_ERROR_MESSAGE_HANDLER(error):
            formatted['message'] = _('Internal server error')

        extensions = OrderedDict([
            ('type', error.__class__.__name__),
            ('code', getattr(error, 'code', 'error')),
            ('timestamp', timegm(datetime.utcnow().utctimetuple())),
        ])

        if hasattr(error, 'error_data'):
            extensions['data'] = error.error_data

        if error.__traceback__ is not None:
            info = error.__traceback__.tb_frame.f_locals.get('info')

            if info is not None:
                extensions['operation'] = info.operation.operation.name

            if settings.DEBUG:
                extensions['trace'] = traceback.format_list(
                    traceback.extract_tb(error.__traceback__),
                )

        formatted['extensions'] = extensions
        return formatted
