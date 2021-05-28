from django.contrib.auth import get_user_model
from django.db.models import Q

from graphql_jwt.decorators import permission_required

from graphene import (ObjectType,
                      Schema,
                      Field,
                      Int,
                      String,
                      List
                      )

from portfolio.gql.types import CategoryType, TaskType
from portfolio.models import Category, Task
from portfolio.gql.mutation import CreateCategory, CreateTask


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


class Mutation(ObjectType):
    create_task = CreateTask.Field()
    create_category = CreateCategory.Field()


schema = Schema(query=Query, mutation=Mutation)