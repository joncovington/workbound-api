from django.contrib.auth import get_user_model
from django.db.models import Q
from graphql_jwt.decorators import permission_required
from graphene import (ObjectType,
                      Schema,
                      Field,
                      Int,
                      String,
                      List,
                      )

from portfolio.gql.types import CategoryType, PortfolioType, TaskType
from portfolio.models import Category, Portfolio, Task
from portfolio.gql.mutation import CreateCategory, CreateTask, UpdateCategory, UpdateTask


User = get_user_model()


class Query(ObjectType):

    # Task queries
    task = Field(TaskType, id=Int())
    tasks = List(TaskType, title=String())

    @permission_required('portfolio.view_task')
    def resolve_task(root, info, id):
        # Querying a single task
        return Task.objects.get(id=id)

    @permission_required('portfolio.view_task')
    def resolve_tasks(root, info, title):
        if title:
            filter = (
                Q(title__icontains=title)
            )
            return Task.objects.filter(filter)
        return Task.objects.all()

    # Category queries
    category = Field(CategoryType, id=Int())
    categories = List(CategoryType, title=String())

    @permission_required('portfolio.view_category')
    def resolve_category(root, info, id):
        # Querying a single category
        return Category.objects.get(id=id)

    @permission_required('portfolio.view_category')
    def resolve_categories(root, info, title):
        if title:
            filter = (
                Q(title__icontains=title)
            )
            return Category.objects.filter(filter)
        return Category.objects.all()

    # Portfolio queries
    portfolio = Field(PortfolioType, id=Int())
    portfolios = List(PortfolioType, portfolio_id=String())

    @permission_required('portfolio.view_portfolio')
    def resolve_portfolio(root, info, id):
        # Querying a single portfolio
        return Portfolio.objects.get(id=id)

    @permission_required('portfolio.view_portfolio')
    def resolve_portfolios(root, info, portfolio_id):
        if portfolio_id:
            filter = (
                Q(portfolio_id__exact=portfolio_id)
            )
            return Portfolio.objects.filter(filter)
        return Portfolio.objects.all()


class Mutation(ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()

    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()


schema = Schema(query=Query, mutation=Mutation)
