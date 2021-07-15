from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from portfolio.models import Portfolio, Section, Category, Task, WorkItem
from portfolio.serializers import (PortfolioSerializer,
                                   SectionSerializer,
                                   CategorySerializer,
                                   TaskSerializer,
                                   WorkItemSerializer
                                   )
from portfolio.permissions import CustomDjangoModelPermissions
from portfolio.filters import PortfolioFilter, SectionFilter, CategoryFilter, WorkItemFilter


User = get_user_model()


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'  # items per page


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

    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    pagination_class = CustomPageNumberPagination
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    filter_fields = ('title', )
    search_fields = ('title', )
    ordering = ('title', )

    def filter_queryset(self, queryset):
        queryset = super(TaskViewSet, self).filter_queryset(queryset)
        print(self.action)
        queryset = queryset.filter(archived=None)
        return queryset

    def perform_create(self, serializer):
        user_id = self.request.data['created_by']
        user = User.objects.get(id=user_id)
        serializer.save(created_by=user)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.archived = timezone.now()
        task.save()
        return Response(data={'status': f'Task {task.id} has been archived'})


class AltTaskViewSet(viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    pagination_class = CustomPageNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering = ('title',)
    search_fields = ('title', )
    queryset = Task.objects.all().filter(archived=None)

    def list(self, request):
        queryset = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        data = [x.id for x in queryset]
        print(data)
        print(type(data))
        return Response(data={'tasks': data}, status=status.HTTP_200_OK)


class WorkItemViewSet(viewsets.ModelViewSet):
    """Manage WorkItems in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, CustomDjangoModelPermissions)
    queryset = WorkItem.objects.all()
    serializer_class = WorkItemSerializer
    filterset_class = WorkItemFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
