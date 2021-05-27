from graphene import ObjectType, Schema
import user.gql.schema as user_gql
import portfolio.gql.schema as portfolio_gql


class Query(portfolio_gql.Query, user_gql.Query, ObjectType):
    pass


class Mutation(portfolio_gql.Mutation, user_gql.Mutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
