import graphene

from .. import schema
from ..testcases import SchemaTestCase


class UpdateGroup(schema.UpdateGroup):

    class Meta:
        lookup_field = 'name'
        lookup_argument = 'name'

    class Arguments:
        name = graphene.String(required=True)


class LookupFieldTests(SchemaTestCase):

    class Mutations(graphene.ObjectType):
        update_group = UpdateGroup.Field()

    def execute(self, arguments):
        query = '''
        mutation UpdateGroup($name: String!) {
          updateGroup(name: $name) {
            group {
              name
            }
          }
        }'''

        return self.client.execute(query, arguments)

    def test_update_group(self):
        self.group.user_set.add(self.user)
        self.client.force_login(self.user)

        response = self.execute({
            'name': self.group.name,
        })

        data = response.data['updateGroup']['group']
        self.assertTrue(data['name'], self.group.name)
