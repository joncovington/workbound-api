from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token

from portfolio.tests.test_workitem_api import sample_task


User = get_user_model()

NO_PERMISSION = 'You do not have permission to perform this action'
USER_CREDENTIALS = {'email': 'test_user@workbound.info', 'password': 'TestPass123'}
ADMIN_CREDENTIALS = {'email': 'test_admin@workbound.info', 'password': 'TestPass123'}


def _sample_user(email=USER_CREDENTIALS['email'], password=USER_CREDENTIALS['password']):
    return User.objects.create_user(email=email, password=password)


def _sample_admin(email=ADMIN_CREDENTIALS['email'], password=ADMIN_CREDENTIALS['password']):
    user = User.objects.create_user(email=email, password=password)
    user.is_superuser = True
    user.save()
    return user


class WorkItemQueryTests(GraphQLTestCase):
    """Graphql WorkItem Query Tests"""

    def test_retreive_all_tasks_with_admin_auth_success(self):
        """Test retrieving all tasks with superuser authorization is successful"""
        task_count = 5
        tasks = [sample_task() for i in range(task_count)]
        user = _sample_admin()
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        gql = """
              query tasks {
                tasks{
                        id
                        title
                        duration
                        created
                        createdBy {
                            id
                            email
                            }
                        archived
                    }
                }
             """
        response = self.query(gql, headers=headers)

        self.assertEqual(len(response.json()['data']['tasks']), len(tasks))
        self.assertResponseNoErrors(response)

    def test_retreive_task_without_auth_fails(self):
        """Test retrieving tasks without authorization is fails"""
        task_count = 5
        [sample_task() for i in range(task_count)]
        gql = """
              query tasks {
                tasks{
                        id
                        title
                        duration
                        created
                        createdBy {
                            id
                            email
                            }
                        archived
                    }
                }
             """
        response = self.query(gql)

        self.assertEqual(response.json()['errors'][0]['message'], NO_PERMISSION)

    # #### Tasks should be visible by all. WorkItems will be filtered by user during query ####
    def test_retreive_tasks_with_perm_success(self):
        """Test retrieving tasks with permissions is successful"""
        user_task_count = 3
        other_task_count = 2
        # Add tasks for our user
        user = _sample_user()
        user_tasks = [sample_task(user=user) for i in range(user_task_count)]

        # Add tasks for another user
        other_user = _sample_user(email='other@workbound.info', password='otherPass123')
        other_tasks = [sample_task(user=other_user) for i in range(other_task_count)]

        # add view permissions for our user
        permission = Permission.objects.get(name='Can view Task')
        user.user_permissions.add(permission)

        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        gql = """
              query tasks {
                tasks{
                        id
                        title
                        duration
                        created
                        createdBy {
                            id
                            email
                            }
                        archived
                    }
                }
             """
        response = self.query(gql, headers=headers)

        self.assertEqual(len(response.json()['data']['tasks']), len(user_tasks) + len(other_tasks))
        self.assertResponseNoErrors(response)


class WorkItemMutationTests(GraphQLTestCase):
    pass
