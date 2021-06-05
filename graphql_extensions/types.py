import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from graphene.types.scalars import Scalar
from graphql.language import ast

from . import exceptions


class Timestamp(Scalar):

    @staticmethod
    def serialize(ts):
        return int(ts.timestamp())

    @staticmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.IntValueNode):
            return cls.parse_value(node.value)

    @staticmethod
    def parse_value(value):
        return datetime.datetime.fromtimestamp(value)


class Email(Scalar):

    @staticmethod
    def serialize(email):
        return str(email)

    @staticmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValueNode):
            return cls.parse_value(node.value)

    @staticmethod
    def parse_value(value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise exceptions.ValidationError(str(e.args[0]))
        return value
