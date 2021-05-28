from random import randrange
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils import timezone
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token

from utils.helpers import sample_id

from portfolio.tests.test_workitem_api import sample_task


User = get_user_model()

NO_PERMISSION = 'You do not have permission to perform this action'
NO_MATCH = 'Task matching query does not exist.'
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

    def test_retreive_tasks_without_auth_fails(self):
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

    def test_retreive_task_with_id_success(self):
        """Test retrieving a task with authorized user is successful"""

        task = sample_task()
        user = _sample_user()
        permission = Permission.objects.get(name='Can view Task')
        user.user_permissions.add(permission)
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'id': task.id}
        gql = """
              query task ($id: Int!){
                        task(id: $id){
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
        response = self.query(gql, headers=headers, variables=variables)

        self.assertEqual(response.json()['data']['task']['id'], task.id)
        self.assertResponseNoErrors(response)

    def test_retreive_task_with_id_no_perm_fail(self):
        """Test retrieving a specific task without permissions fails"""

        task = sample_task()
        user = _sample_user()

        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'id': task.id}
        gql = """
              query task ($id: Int!){
                        task(id: $id){
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
        response = self.query(gql, headers=headers, variables=variables)

        self.assertEqual(response.json()['errors'][0]['message'], NO_PERMISSION)

    def test_retreive_task_incorrect_params_vals_fails(self):
        """Test retrieving a task with bad value fails"""

        task = sample_task()
        user = _sample_user()
        permission = Permission.objects.get(name='Can view Task')
        user.user_permissions.add(permission)
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'id': task.id + 1}
        gql = """
              query task ($id: Int!){
                        task(id: $id){
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
        response = self.query(gql, headers=headers, variables=variables)

        self.assertEqual(response.json()['errors'][0]['message'], NO_MATCH)


class WorkItemMutationTests(GraphQLTestCase):
    """Graphql WorkItem Mutation Tests"""

    def test_create_task_with_permissions_success(self):
        """Test creating a task with correct permissions is successful"""
        user = _sample_user()
        permission = Permission.objects.get(name='Can add Task')
        user.user_permissions.add(permission)
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'title': sample_id(size=10),
                     'description': sample_id(size=20),
                     'duration': 10,
                     'createdById': user.id
                     }
        gql = """
              mutation createTask($title: String!,
                                  $description: String!,
                                  $duration: Int!,
                                  $createdById: Int!) {
                createTask(title: $title,
                           description: $description,
                           duration: $duration,
                           createdById: $createdById){
                    task{
                        id
                        title
                        description
                        duration
                        created
                        createdBy{
                            id
                            email
                        }
                        archived
                        }
                    }
                }
             """
        response = self.query(gql, headers=headers, variables=variables)
        task = response.json()['data']['createTask']['task']

        self.assertResponseNoErrors(response)
        self.assertEqual(task['createdBy']['email'], user.email)
        self.assertEqual(task['title'], variables['title'])

    def test_create_task_without_permissions_fails(self):
        """Test creating a task without permissions fails"""
        user = _sample_user()
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'title': sample_id(size=10),
                     'description': sample_id(size=20),
                     'duration': 10,
                     'createdById': user.id
                     }
        gql = """
              mutation createTask($title: String!,
                                  $description: String!,
                                  $duration: Int!,
                                  $createdById: Int!) {
                createTask(title: $title,
                           description: $description,
                           duration: $duration,
                           createdById: $createdById){
                    task{
                        id
                        title
                        description
                        duration
                        created
                        createdBy{
                            id
                            email
                        }
                        archived
                        }
                    }
                }
             """
        response = self.query(gql, headers=headers, variables=variables)

        self.assertEqual(response.json()['errors'][0]['message'], NO_PERMISSION)

    def test_update_task_with_perm_successful(self):
        """Test updating a task with correct permissions is successful"""
        user = _sample_user()
        permission = Permission.objects.get(name='Can change Task')
        user.user_permissions.add(permission)
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        task = sample_task(user=user)

        # make sure we generate a new title
        new_title = task.title
        while task.title is new_title:
            new_title = sample_id(size=10)

        new_archived_date = timezone.now().isoformat()

        variables = {'id': task.id,
                     'title': new_title,
                     'description': sample_id(size=20),
                     'duration': randrange(10),
                     'archived': new_archived_date
                     }
        gql = """
              mutation updateTask($id: Int!
                                  $title: String!,
                                  $description: String!,
                                  $duration: Int!,
                                  $archived: DateTime!) {
                updateTask(id: $id,
                           title: $title,
                           description: $description,
                           duration: $duration,
                           archived: $archived){
                    task{
                        id
                        title
                        description
                        duration
                        created
                        createdBy{
                            id
                            email
                        }
                        archived
                        }
                    }
                }
             """
        response = self.query(gql, headers=headers, variables=variables)
        updated_task = response.json()['data']['updateTask']['task']

        self.assertResponseNoErrors(response)
        # Task id should be the same
        self.assertEqual(updated_task['id'], task.id)
        # Task title should be updated
        self.assertEqual(updated_task['title'], variables['title'])
        # Returned task title isn't the old task model title
        self.assertNotEqual(updated_task['title'], task.title)

    def test_update_task_without_perm_fails(self):
        """Test updating a task without permissions fails"""
        user = _sample_user()

        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        task = sample_task(user=user)

        # make sure we generate a new title
        new_title = task.title
        while task.title is new_title:
            new_title = sample_id(size=10)

        variables = {'id': task.id,
                     'title': new_title,
                     'description': sample_id(size=20),
                     'duration': randrange(10),
                     }
        gql = """
              mutation updateTask($id: Int!
                                  $title: String!,
                                  $description: String!,
                                  $duration: Int!) {
                updateTask(id: $id,
                           title: $title,
                           description: $description,
                           duration: $duration){
                    task{
                        id
                        title
                        description
                        duration
                        created
                        createdBy{
                            id
                            email
                        }
                        archived
                        }
                    }
                }
             """
        response = self.query(gql, headers=headers, variables=variables)

        self.assertEqual(response.json()['errors'][0]['message'], NO_PERMISSION)
