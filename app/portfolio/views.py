from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from portfolio.models import Portfolio, Section, SectionCategory, Task, WorkItem
from portfolio.serializers import (PortfolioSerializer,
                                   SectionSerializer,
                                   SectionCategorySerializer,
                                   TaskSerializer,
                                   WorkItemSerializer
                                   )
from portfolio.permissions import CustomDjangoModelPermissions


class PortfolioViewSet(viewsets.ModelViewSet):
    """Manage Portfolios in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SectionViewSet(viewsets.ModelViewSet):
    """Manage Sections in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SectionCategoryViewSet(viewsets.ModelViewSet):
    """Manage Sections in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = SectionCategory.objects.all()
    serializer_class = SectionCategorySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """Manage Tasks in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class WorkItemViewSet(viewsets.ModelViewSet):
    """Manage WorkItems in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = WorkItem.objects.all()
    serializer_class = WorkItemSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
