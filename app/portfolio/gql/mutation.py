from django.contrib.auth import get_user_model
from graphql_jwt.decorators import permission_required
from graphene import (Mutation,
                      Field,
                      Int,
                      String,
                      DateTime,
                      )

from portfolio.gql.types import CategoryType, PortfolioType, TaskType
from portfolio.models import Category, Portfolio, Task
from portfolio.serializers import CategorySerializer, PortfolioSerializer, TaskSerializer

User = get_user_model()


class CreateTask(Mutation):
    """Graphql mutation using serializer to create a Task"""
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        duration = Int(required=True)
        created_by_id = Int(required=True)

    task = Field(TaskType)

    @classmethod
    @permission_required('portfolio.add_task')
    def mutate(cls, root, info, **kwargs):
        serializer_data = kwargs
        serializer_data['created_by'] = kwargs.pop('created_by_id')
        serializer = TaskSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        return CreateTask(task=serializer.save())


class UpdateTask(Mutation):
    """Graphql mutation to update a Task"""
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        duration = Int()
        archived = DateTime()

    task = Field(TaskType)

    @classmethod
    @permission_required('portfolio.change_task')
    def mutate(cls, root, info, **kwargs):
        task_instance = Task.objects.get(id=kwargs['id'])
        serializer = TaskSerializer(instance=task_instance, data=kwargs)
        serializer.is_valid(raise_exception=True)
        return UpdateTask(task=serializer.save())


class CreateCategory(Mutation):
    """Graphql mutation to create a Category"""
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        created_by_id = Int(required=True)

    category = Field(CategoryType)

    @classmethod
    @permission_required('portfolio.add_category')
    def mutate(cls, root, info, **kwargs):
        serializer_data = kwargs
        serializer_data['created_by'] = kwargs.pop('created_by_id')
        serializer = CategorySerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        return CreateCategory(category=serializer.save())


class UpdateCategory(Mutation):
    """Graphql mutation to update a category"""
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        archived = DateTime()

    category = Field(CategoryType)

    @classmethod
    @permission_required('portfolio.change_category')
    def mutate(cls, root, info, **kwargs):
        category_instance = Category.objects.get(id=kwargs['id'])
        serializer = CategorySerializer(instance=category_instance, data=kwargs)
        serializer.is_valid(raise_exception=True)
        return UpdateCategory(category=serializer.save())


class CreatePortfolio(Mutation):
    """Graphql mutation using serializer to create a Portfolio"""
    class Arguments:
        reference = String()
        created_by_id = Int(required=True)

    portfolio = Field(PortfolioType)

    @classmethod
    @permission_required('portfolio.add_portfolio')
    def mutate(cls, root, info, **kwargs):
        serializer_data = kwargs
        serializer_data['created_by'] = kwargs.pop('created_by_id')
        serializer = PortfolioSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        return CreatePortfolio(portfolio=serializer.save())


class UpdatePortfolio(Mutation):
    """Graphql mutation to update a portfolio"""
    class Arguments:
        id = Int(required=True)
        reference = String()
        completed = DateTime()

    portfolio = Field(PortfolioType)

    @classmethod
    @permission_required('portfolio.change_portfolio')
    def mutate(cls, root, info, **kwargs):
        portfolio_instance = Portfolio.objects.get(id=kwargs['id'])
        # Don't change the created_by field
        kwargs['created_by'] = portfolio_instance.created_by.id
        serializer = PortfolioSerializer(instance=portfolio_instance, data=kwargs)
        serializer.is_valid(raise_exception=True)
        return UpdatePortfolio(portfolio=serializer.save())
