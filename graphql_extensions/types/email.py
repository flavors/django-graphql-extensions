from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from graphene.types.scalars import Scalar
from graphql.language import ast

from .. import exceptions


class Email(Scalar):

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
            validate_email(value)
        except ValidationError as err:
            raise exceptions.ValidationError(str(err))
        return value
