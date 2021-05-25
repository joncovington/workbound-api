import graphene
import user.gql.schema as user_gql


class Query(user_gql.Query, graphene.ObjectType):
    pass


class Mutation(user_gql.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
