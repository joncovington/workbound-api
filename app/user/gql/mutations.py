from django.contrib.auth import get_user_model

import graphene
from graphene.types.mutation import Mutation

from user.gql.types import UserType

User = get_user_model()


class UserCreate(Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()
        return UserCreate(user=user)
