import datetime

from graphene.types.scalars import Scalar
from graphql.language import ast


class Timestamp(Scalar):

    @classmethod
    def serialize(cls, value):
        return value.timestamp()

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.FloatValue):
            return cls.parse_value(node.value)

    @classmethod
    def parse_value(cls, value):
        return datetime.datetime.fromtimestamp(value)
