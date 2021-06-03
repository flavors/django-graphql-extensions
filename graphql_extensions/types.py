import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from graphene.types.scalars import Scalar
from graphql.language import ast

from . import exceptions


class Timestamp(Scalar):

    @classmethod
    def serialize(cls, value):
        return int(value.timestamp())

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.IntValueNode):
            return cls.parse_value(node.value)

    @classmethod
    def parse_value(cls, value):
        return datetime.datetime.fromtimestamp(value)


class Email(Scalar):

    @classmethod
    def serialize(cls, value):
        return str(value)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValueNode):
            return cls.parse_value(node.value)

    @classmethod
    def parse_value(cls, value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise exceptions.ValidationError(str(e.args[0]))
        return value
