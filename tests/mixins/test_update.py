from ..testcases import GroupTestCase


class UpdateMixinTests(GroupTestCase):

    def execute(self, arguments):
        query = '''
        mutation UpdateGroup($id: Int!, $name: String!) {
          updateGroup(id: $id, name: $name) {
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
            'id': self.group.pk,
            'name': '-updated-',
        })

        data = response.data['updateGroup']['group']
        self.assertTrue(data['name'], '-updated-')

    def test_update_group_not_found(self):
        self.group.user_set.add(self.user)
        self.client.force_login(self.user)

        response = self.execute({
            'id': 0,
            'name': '-updated-',
        })

        self.assertTrue(response.errors)

    def test_update_group_login_required(self):
        self.group.user_set.add(self.user)

        response = self.execute({
            'id': self.group.pk,
            'name': '-updated-',
        })

        self.assertTrue(response.errors)

    def test_syntax_error(self):
        response = self.client.execute('mutation')
        self.assertTrue(response.errors)
