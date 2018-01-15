from django.utils.translation import ugettext as _

from graphene.types.scalars import Scalar
from graphql.language import ast
from graphql_relay import from_global_id

from .. import exceptions


class GlobalID(Scalar):

    @classmethod
    def serialize(cls, value):
        return str(value)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            return cls.parse_value(node.value)

    @classmethod
    def parse_value(cls, value):
        try:
            _type, _id = from_global_id(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(_('ID cannot be resolved'))
        return int(_id)
