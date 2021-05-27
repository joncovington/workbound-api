from django.contrib.auth import get_user_model

import graphene
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh
from graphql_jwt.decorators import login_required

from user.gql.types import UserType
from user.gql.mutations import CreateUser

User = get_user_model()


class Query(graphene.ObjectType):
    current_user = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(root, info):
        return User.objects.all()

    @login_required
    def resolve_current_user(root, info):
        user = info.context.user
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
