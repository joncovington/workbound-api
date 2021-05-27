from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


User = get_user_model()

NO_PERMISSION = 'You do not have permission to perform this action'
BAD_CREDENTIALS = 'Please enter valid credentials'


def _sample_user(email, password):
    return User.objects.create_user(email=email, password=password)


class UserMutationTests(GraphQLTestCase):

    def test_retrieve_token_successful(self):
        """Test obtaining auth token with valid credentials is successful"""
        user = _sample_user('test@workbound.info', 'TestPass123')
        gql = """
              mutation tokenAuth($email: String!, $password: String!){
                tokenAuth(email: $email, password: $password){
                token
                payload
                }
              }
             """
        response = self.query(gql, variables={'email': user.email, 'password': 'TestPass123'})

        self.assertEqual(response.json()['data']['tokenAuth']['payload']['email'], user.email)
        self.assertResponseNoErrors(response)

    def test_retrieve_token_bad_credentials_fails(self):
        """Test obtaining auth token with invalid credentials fails"""
        user = _sample_user('test@workbound.info', 'TestPass123')
        gql = """
              mutation tokenAuth($email: String!, $password: String!){
                tokenAuth(email: $email, password: $password){
                token
                payload
                }
              }
             """
        response = self.query(gql, variables={'email': user.email, 'password': 'wrongPass'})

        self.assertEqual(response.json()['errors'][0]['message'], BAD_CREDENTIALS)

    def test_retreive_current_user_success(self):
        """Test retrieving a user with authorization is successful"""
        user = _sample_user('test@workbound.info', 'TestPass123')
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        gql = """
              query User {
                currentUser {
                    id
                    email
                }
               }
             """
        response = self.query(gql, headers=headers)

        self.assertEqual(response.json()['data']['currentUser']['email'], user.email)
        self.assertResponseNoErrors(response)

    def test_retrieve_current_user_without_token_fails(self):
        """Test retrieving a user without authorization gives permissions error"""
        gql = """
              query User {
                currentUser {
                    id
                    email
                }
               }
             """
        response = self.query(gql)

        self.assertEqual(response.json()['errors'][0]['message'], NO_PERMISSION)
