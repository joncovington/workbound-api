from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from portfolio.models import Portfolio, Section, SectionCategory
from portfolio.serializers import PortfolioSerializer, SectionSerializer, SectionCategorySerializer
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
