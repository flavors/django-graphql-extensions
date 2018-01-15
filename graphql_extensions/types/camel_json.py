from graphene.types.generic import GenericScalar

from ..utils import dashed_to_camel


class CamelJSON(GenericScalar):

    @classmethod
    def serialize(cls, value):
        return dashed_to_camel(value)
