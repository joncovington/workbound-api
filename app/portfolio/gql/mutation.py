from datetime import datetime
from django.contrib.auth import get_user_model

from graphql_jwt.decorators import permission_required
from graphene import (Mutation,
                      Field,
                      Int,
                      String,
                      DateTime,
                      )


from portfolio.gql.types import CategoryType, TaskType
from portfolio.models import Category, Task
from portfolio.serializers import CategorySerializer, TaskSerializer

User = get_user_model()


# class CreateTask(Mutation):
#     """Graphql mutation to create a Task"""
#     class Arguments:
#         title = String(required=True)
#         description = String(required=True)
#         duration = Int(required=True)
#         created_by_id = Int(required=True)

#     task = Field(TaskType)

#     @classmethod
#     @permission_required('portfolio.add_task')
#     def mutate(cls, root, info, **kwargs):
#         user_id = kwargs.pop('created_by_id')
#         user = User.objects.get(id=user_id)
#         task = Task.objects.create(created_by=user, **kwargs)
#         task.save()
#         return cls(task=task)


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
        cat_id = kwargs.pop('id')
        category = Category.objects.get(id=cat_id)
        if hasattr(kwargs, 'archived'):
            archived_date = datetime.fromisoformat(kwargs.pop(['archived']))
            category.archived = archived_date

        for k, v in kwargs.items():
            if k in [field.name for field in category._meta.get_fields()]:
                setattr(category, k, v)
        category.save()
        return cls(category=category)
