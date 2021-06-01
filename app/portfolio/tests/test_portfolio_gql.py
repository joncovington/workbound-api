from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token

from utils.helpers import sample_id

from portfolio.tests.test_portfolio_api import sample_portfolio


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


class PortfolioQueryTests(GraphQLTestCase):
    """Graphql Portfolio Query Tests"""

    def test_retreive_all_portfolios_with_admin_auth_success(self):
        """Test retrieving all portfolios with superuser authorization is successful"""
        portfolio_count = 5
        portfolios = [sample_portfolio() for i in range(portfolio_count)]
        user = _sample_admin()
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        gql = """
              query portfolios {
                portfolios{
                        id
                        portfolioId
                        created
                        createdBy {
                            id
                            email
                            }
                        completed
                    }
                }
             """
        response = self.query(gql, headers=headers)

        self.assertEqual(len(response.json()['data']['portfolios']), len(portfolios))
        self.assertResponseNoErrors(response)

    def test_retreive_all_portfolios_without_auth_fails(self):
        """Test retrieving all portfolios without authorization is fails"""
        portfolio_count = 5
        [sample_portfolio() for i in range(portfolio_count)]
        gql = """
              query portfolios {
                portfolios{
                        id
                        portfolioId
                        created
                        createdBy {
                            id
                            email
                            }
                        completed
                    }
                }
             """
        response = self.query(gql)

        self.assertEqual(response.json()['errors'][0]['message'], NO_PERMISSION)

    def test_retreive_portfolios_with_perm_success(self):
        """Test retrieving portfolios with permissions is successful"""
        user_portfolio_count = 3
        other_portfolio_count = 2
        # Add portfolios for our user
        user = _sample_user()
        user_portfolios = [sample_portfolio(user=user) for i in range(user_portfolio_count)]

        # Add portfolios for another user
        other_user = _sample_user(email='other@workbound.info', password='otherPass123')
        other_portfolios = [sample_portfolio(user=other_user) for i in range(other_portfolio_count)]

        # add view permissions for our user
        permission = Permission.objects.get(name='Can view Portfolio')
        user.user_permissions.add(permission)

        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        gql = """
              query portfolios {
                portfolios{
                        id
                        portfolioId
                        created
                        createdBy {
                            id
                            email
                            }
                        completed
                    }
                }
             """
        response = self.query(gql, headers=headers)

        self.assertEqual(len(response.json()['data']['portfolios']), len(user_portfolios) + len(other_portfolios))
        self.assertResponseNoErrors(response)

    def test_retreive_portfolio_with_id_success(self):
        """Test retrieving portfolios with permissions is successful"""

        user = _sample_user()
        portfolio = sample_portfolio(user=user)

        # add view permissions for our user
        permission = Permission.objects.get(name='Can view Portfolio')
        user.user_permissions.add(permission)

        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'id': portfolio.id}
        gql = """
              query portfolio($id: Int!) {
                portfolio(id: $id){
                        id
                        portfolioId
                        created
                        createdBy {
                            id
                            email
                            }
                        completed
                    }
                }
             """
        response = self.query(gql, headers=headers, variables=variables)

        self.assertEqual(response.json()['data']['portfolio']['id'], portfolio.id)
        self.assertResponseNoErrors(response)


class PortfolioMutationTests(GraphQLTestCase):
    """Graphql Portfolio Mutation Tests"""

    def test_create_portfolio_with_permissions_success(self):
        """Test creating a portfolio with correct permissions is successful"""
        user = _sample_user()
        permission = Permission.objects.get(name='Can add Portfolio')
        user.user_permissions.add(permission)
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'reference': sample_id(size=10),
                     'createdById': user.id
                     }
        gql = """
              mutation createPortfolio($reference: String!
                                  $createdById: Int!) {
                createPortfolio(reference: $reference,
                           createdById: $createdById){
                    portfolio{
                        id
                        portfolioId
                        reference
                        created
                        createdBy{
                            id
                            email
                        }
                        completed
                        }
                    }
                }
             """
        response = self.query(gql, headers=headers, variables=variables)
        portfolio = response.json()['data']['createPortfolio']['portfolio']
        self.assertResponseNoErrors(response)
        self.assertEqual(portfolio['createdBy']['email'], user.email)
        self.assertEqual(portfolio['reference'], variables['reference'])

    def test_create_portfolio_without_permissions_fails(self):
        """Test creating a portfolio without permissions is fails"""
        user = _sample_user()
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        variables = {'reference': sample_id(size=10),
                     'createdById': user.id
                     }
        gql = """
              mutation createPortfolio($reference: String!
                                  $createdById: Int!) {
                createPortfolio(reference: $reference,
                           createdById: $createdById){
                    portfolio{
                        id
                        portfolioId
                        reference
                        created
                        createdBy{
                            id
                            email
                        }
                        completed
                        }
                    }
                }
             """
        response = self.query(gql, headers=headers, variables=variables)

        self.assertEqual(response.json()['errors'][0]['message'], NO_PERMISSION)
