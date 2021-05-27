from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


User = get_user_model()


def _sample_user(email, password):
    return User.objects.create_user(email=email, password=password)


class UserMutationTests(GraphQLTestCase):

    def test_retrieve_token(self):
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

    def test_retreive_current_user(self):
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
