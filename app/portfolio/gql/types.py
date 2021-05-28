from graphene import Int
from graphene_django import DjangoObjectType

from portfolio.models import Category, Task


class TaskType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = Task


class CategoryType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = Category
