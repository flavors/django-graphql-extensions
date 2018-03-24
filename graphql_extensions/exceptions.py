from django.utils.translation import ugettext_lazy as _


class GraphQLError(Exception):
    default_message = _('A server error occurred')
    default_code = 'error'

    def __init__(self, message=None, code=None, **data):
        if message is None:
            message = self.default_message

        if code is None:
            code = self.default_code

        self.code = code
        self.error_data = data

        super().__init__(message)


class PermissionDenied(GraphQLError):
    default_message = _('You do not have permission to perform this action')
    default_code = 'permissionDenied'


class ValidationError(GraphQLError):
    default_message = _('Invalid input')
    default_code = 'invalid'


class NotFound(GraphQLError):
    default_message = _('GraphQL object not found')
    default_code = 'notFound'
