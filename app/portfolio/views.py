from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from portfolio.models import Portfolio, Section, Category, Task, WorkItem
from portfolio.serializers import (PortfolioSerializer,
                                   SectionSerializer,
                                   CategorySerializer,
                                   TaskSerializer,
                                   WorkItemSerializer
                                   )
from portfolio.permissions import CustomDjangoModelPermissions
from portfolio.filters import PortfolioFilter, SectionFilter, TaskFilter, CategoryFilter, WorkItemFilter


class PortfolioViewSet(viewsets.ModelViewSet):
    """Manage Portfolios in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    filterset_class = PortfolioFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SectionViewSet(viewsets.ModelViewSet):
    """Manage Sections in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filterset_class = SectionFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage Sections in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter


class TaskViewSet(viewsets.ModelViewSet):
    """Manage Tasks in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class WorkItemViewSet(viewsets.ModelViewSet):
    """Manage WorkItems in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = WorkItem.objects.all()
    serializer_class = WorkItemSerializer
    filterset_class = WorkItemFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
