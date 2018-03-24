from django.utils.translation import ugettext as _

from graphene.types.scalars import Scalar
from graphql.language import ast

from .. import exceptions


class Choices(Scalar):

    @classmethod
    def serialize(cls, value):
        return str(value)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            return cls.parse_value(node.value)

    @classmethod
    def parse_value(cls, value):
        choices = cls.CHOICES

        if hasattr(choices, '_identifier_map'):
            choices = choices._identifier_map

        if value not in choices:
            raise exceptions.ValidationError(
                _('Invalid choice \'{}\'').format(value),
            )
        return value
