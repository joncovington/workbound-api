from django.contrib.auth import get_user_model
from graphql_jwt.decorators import permission_required

from graphene import (Mutation,
                      Field,
                      Int,
                      String,
                      )


from portfolio.gql.types import TaskType
from portfolio.models import Task

User = get_user_model()


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
