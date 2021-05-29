from graphene import Int, relay
from graphene_django import DjangoObjectType

from portfolio.models import Category, Task


class TaskType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = Task


class TaskNode(DjangoObjectType):
    pk = Int(source='id')

    class Meta:
        model = Task
        fields = ['title', 'description', 'duration', ]
        interfaces = (relay.Node, )


class CategoryType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = Category


class CategoryNode(DjangoObjectType):
    pk = Int(source='id')

    class Meta:
        model = Category
        fields = ['title', 'description', 'duration', ]
        interfaces = (relay.Node, )
