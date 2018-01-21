from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

import graphene
from graphene_django import DjangoObjectType

from graphql_extensions import mixins
from graphql_extensions.auth.decorators import login_required


class UserType(DjangoObjectType):

    class Meta:
        model = get_user_model()


class GroupType(DjangoObjectType):

    class Meta:
        model = Group


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user


class UpdateGroupMutation(mixins.UpdateMixin, graphene.Mutation):
    group = graphene.Field(GroupType)

    class Meta:
        abstract = True

    @classmethod
    def get_queryset(cls, info, **kwargs):
        return info.context.user.groups.all()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        group = cls.update(info, **kwargs)
        return cls(group=group)


class UpdateGroup(UpdateGroupMutation):

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()


class UpdateGroupLookup(UpdateGroupMutation):

    class Meta:
        lookup_field = 'name'
        lookup_argument = 'name'

    class Arguments:
        name = graphene.String(required=True)


class Mutations(graphene.ObjectType):
    update_group = UpdateGroup.Field()
    update_group_lookup = UpdateGroupLookup.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
