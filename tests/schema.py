from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from graphql_extensions.decorators import login_required


class UserType(DjangoObjectType):

    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType)

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return info.context.user
