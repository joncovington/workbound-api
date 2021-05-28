from graphene import Int
from graphene_django import DjangoObjectType

from portfolio.models import Task


class TaskType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = Task
