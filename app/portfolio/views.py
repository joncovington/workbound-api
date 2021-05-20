from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from portfolio.models import Portfolio, Section
from portfolio.serializers import PortfolioSerializer, SectionSerializer


class PortfolioPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm(
                'portfolio.view_portfolio'
            )
        if request.method == 'POST':
            return request.user.has_perm(
                'portfolio.add_portfolio'
            )


class PortfolioViewSet(viewsets.ModelViewSet):
    """Manage Portfolios in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, PortfolioPermission)
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SectionPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm(
                'portfolio.view_section'
            )
        if request.method == 'POST':
            return request.user.has_perm(
                'portfolio.add_section'
            )


class SectionViewSet(viewsets.ModelViewSet):
    """Manage Sections in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, SectionPermission)
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
