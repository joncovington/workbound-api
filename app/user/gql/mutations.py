from django.contrib.auth import get_user_model

import graphene
from graphene.types.mutation import Mutation
from graphql_jwt.decorators import login_required, permission_required

from user.gql.types import UserType

User = get_user_model()


class CreateUser(Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @login_required
    @permission_required('core.add_customuser')
    def mutate(self, info, email, password):
        user = User.objects.create_user(email=email, password=password)
        return CreateUser(user=user)
