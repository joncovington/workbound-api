from django.contrib.auth import get_user_model
from django.db.models import Q

from graphql_jwt.decorators import permission_required

from graphene import (ObjectType,
                      Schema,
                      Mutation,
                      Field,
                      Int,
                      String,
                      )
from graphene.types.structures import List
from graphene_django import DjangoObjectType

from portfolio.gql.types import TaskType
from portfolio.models import Task

from user.gql.types import UserType


User = get_user_model()


class TaskNode(DjangoObjectType):
    created_by = Field(UserType)

    class Meta:
        model = Task
        filter_fields = ['title', ]


class Query(ObjectType):
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


class CreateTask(Mutation):

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


class Mutation(ObjectType):
    create_task = CreateTask.Field()


schema = Schema(query=Query, mutation=Mutation)
