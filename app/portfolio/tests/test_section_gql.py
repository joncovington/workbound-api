from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token

from utils.helpers import sample_id

from portfolio.tests.test_section_api import sample_category


User = get_user_model()

NO_PERMISSION = 'You do not have permission to perform this action'
NO_MATCH = 'Category matching query does not exist.'
USER_CREDENTIALS = {'email': 'test_user@workbound.info', 'password': 'TestPass123'}
ADMIN_CREDENTIALS = {'email': 'test_admin@workbound.info', 'password': 'TestPass123'}


def _sample_user(email=USER_CREDENTIALS['email'], password=USER_CREDENTIALS['password']):
    return User.objects.create_user(email=email, password=password)


def _sample_admin(email=ADMIN_CREDENTIALS['email'], password=ADMIN_CREDENTIALS['password']):
    user = User.objects.create_user(email=email, password=password)
    user.is_superuser = True
    user.save()
    return user


class SectionQueryTests(GraphQLTestCase):
    """Graphql Section Query Tests"""

    def test_retreive_all_categories_with_admin_auth_success(self):
        """Test retrieving all categories with superuser authorization is successful"""
        category_count = 5
        categories = [sample_category() for i in range(category_count)]
        user = _sample_admin()
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        gql = """
              query categories {
                categories{
                        id
                        title
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

        self.assertEqual(len(response.json()['data']['categories']), len(categories))
        self.assertResponseNoErrors(response)

    def test_retreive_categories_without_auth_fails(self):
        """Test retrieving categories without authorization is fails"""
        category_count = 5
        [sample_category() for i in range(category_count)]
        gql = """
              query categories {
                categories{
                        id
                        title
                        description
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

    # #### Categories should be visible by all. Sections will be filtered by user during query ####
    def test_retreive_categories_with_perm_success(self):
        """Test retrieving categories with permissions is successful"""
        user_category_count = 3
        other_category_count = 2
        # Add categories for our user
        user = _sample_user()
        user_categories = [sample_category(user=user) for i in range(user_category_count)]

        # Add categories for another user
        other_user = _sample_user(email='other@workbound.info', password='otherPass123')
        other_categories = [sample_category(user=other_user) for i in range(other_category_count)]

        # add view permissions for our user
        permission = Permission.objects.get(name='Can view Category')
        user.user_permissions.add(permission)

        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        gql = """
              query categories {
                categories{
                        id
                        title
                        description
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

        self.assertEqual(len(response.json()['data']['categories']), len(user_categories) + len(other_categories))
        self.assertResponseNoErrors(response)

    def test_retreive_category_with_id_success(self):
        """Test retrieving a category with authorized user is successful"""

        category = sample_category()
        user = _sample_user()
        permission = Permission.objects.get(name='Can view Category')
        user.user_permissions.add(permission)
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'id': category.id}
        gql = """
              query category ($id: Int!){
                        category(id: $id){
                            id
                            title
                            description
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

        self.assertEqual(response.json()['data']['category']['id'], category.id)
        self.assertResponseNoErrors(response)

    def test_retreive_category_with_id_no_perm_fail(self):
        """Test retrieving a specific category without permissions fails"""

        category = sample_category()
        user = _sample_user()

        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'id': category.id}
        gql = """
              query category ($id: Int!){
                        category(id: $id){
                            id
                            title
                            description
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

    def test_retreive_category_incorrect_params_vals_fails(self):
        """Test retrieving a category with bad value fails"""

        category = sample_category()
        user = _sample_user()
        permission = Permission.objects.get(name='Can view Category')
        user.user_permissions.add(permission)
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'id': category.id + 1}
        gql = """
              query category ($id: Int!){
                        category(id: $id){
                            id
                            title
                            description
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


class SectionMutationTests(GraphQLTestCase):
    """Graphql Section Mutation Tests"""

    def test_create_category_with_permissions_success(self):
        """Test creating a category with correct permissions is successful"""
        user = _sample_user()
        permission = Permission.objects.get(name='Can add Category')
        user.user_permissions.add(permission)
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'title': sample_id(size=10),
                     'description': sample_id(size=20),
                     'createdById': user.id
                     }
        gql = """
              mutation createCategory($title: String!,
                                  $description: String!,
                                  $createdById: Int!) {
                createCategory(title: $title,
                           description: $description,
                           createdById: $createdById){
                    category{
                        id
                        title
                        description
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
        category = response.json()['data']['createCategory']['category']

        self.assertResponseNoErrors(response)
        self.assertEqual(category['createdBy']['email'], user.email)
        self.assertEqual(category['title'], variables['title'])

    def test_create_category_without_permissions_fails(self):
        """Test creating a category without permissions fails"""
        user = _sample_user()
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'title': sample_id(size=10),
                     'description': sample_id(size=20),
                     'createdById': user.id
                     }
        gql = """
              mutation createCategory($title: String!,
                                  $description: String!,
                                  $createdById: Int!) {
                createCategory(title: $title,
                           description: $description,
                           createdById: $createdById){
                    category{
                        id
                        title
                        description
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
