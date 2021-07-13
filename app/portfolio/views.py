from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from portfolio.models import Portfolio, Section, Category, Task, WorkItem
from portfolio.serializers import (BuildSerializer, PortfolioSerializer,
                                   SectionSerializer,
                                   CategorySerializer,
                                   TaskSerializer,
                                   WorkItemSerializer
                                   )
from portfolio.permissions import BuildPermission, CustomDjangoModelPermissions
from portfolio.filters import PortfolioFilter, SectionFilter, TaskFilter, CategoryFilter, WorkItemFilter


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
    queryset = Task.objects.all().order_by('title')
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


class BuildView(APIView):
    permission_classes = (IsAuthenticated, BuildPermission)
    serializer_class = BuildSerializer

    # def get(self, request, *args, **kwargs):
    #     payload = {
    #         'build': [
    #             {
    #                 'category': 1,
    #                 'tasks': [1, 2],
    #             }
    #         ]
    #     }
    #     data = json.dumps(payload)
    #     return response.Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email='admin@workbound.info')
        print(request.data)
        build = request.data['build']
        if len(build) > 0:
            portfolio = Portfolio.objects.create(created_by=user)
            for section in build:
                category = Category.objects.get(id=int(build['category']))
                section = Section.objects.create(created_by=user, category=category, portfolio=portfolio)
                for task_id in build['tasks']:
                    task = Task.objects.get(id=task_id)
                    WorkItem.objects.create(section=section, task=task, created_by=user)
            serializer = PortfolioSerializer(portfolio)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
