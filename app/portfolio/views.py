from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from portfolio.models import Portfolio
from portfolio.serializers import PortfolioSerializer


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


class PortfolioViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin):
    """Manage Portfolios in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, PortfolioPermission)
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
