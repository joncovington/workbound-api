from graphene_django import DjangoObjectType

from portfolio.models import Task


class TaskType(DjangoObjectType):

    class Meta:
        model = Task
