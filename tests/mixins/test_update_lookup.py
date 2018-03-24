from ..testcases import GroupTestCase


class RetrieveMixinTests(GroupTestCase):

    def execute(self, arguments):
        query = '''
        mutation UpdateGroupLookup($name: String!) {
          updateGroupLookup(name: $name) {
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

        data = response.data['updateGroupLookup']['group']
        self.assertTrue(data['name'], self.group.name)
