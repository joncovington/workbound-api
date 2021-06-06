from graphene import Int
from graphene.types.structures import List
from graphene_django import DjangoObjectType

from portfolio.models import Category, Portfolio, Section, Task, WorkItem


class TaskType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = Task


class CategoryType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = Category


class WorkItemType(DjangoObjectType):
    id = Int(source='id')

    class Meta:
        model = WorkItem


class SectionType(DjangoObjectType):
    id = Int(source='id')
    workitems = List(WorkItemType)

    class Meta:
        model = Section

    def resolve_workitems(self, info):
        workitems = self.workitems.all()
        return workitems


class PortfolioType(DjangoObjectType):
    id = Int(source='id')
    sections = List(SectionType)

    class Meta:
        model = Portfolio

    def resolve_sections(self, info):
        sections = self.sections.all()
        return sections
