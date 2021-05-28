from django.contrib.auth import get_user_model
from graphql_jwt.decorators import permission_required

from graphene import (Mutation,
                      Field,
                      Int,
                      String,
                      )


from portfolio.gql.types import CategoryType, TaskType
from portfolio.models import Category, Task

User = get_user_model()


class CreateTask(Mutation):
    """Graphql mutation to create a Task"""
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        duration = Int(required=True)
        created_by_id = Int(required=True)

    task = Field(TaskType)

    @classmethod
    @permission_required('portfolio.add_task')
    def mutate(cls, root, info, **kwargs):
        user_id = kwargs.pop('created_by_id')
        user = User.objects.get(id=user_id)
        task = Task.objects.create(created_by=user, **kwargs)
        task.save()
        return cls(task=task)


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
        user_id = kwargs.pop('created_by_id')
        user = User.objects.get(id=user_id)
        category = Category.objects.create(created_by=user, **kwargs)
        category.save()
        return cls(category=category)
