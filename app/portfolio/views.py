from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from portfolio.models import Portfolio
from portfolio.serializers import PortfolioSerializer


class PortfolioPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(
            'portfolio.view_portfolio'
        )


class PortfolioViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Portfolios in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, PortfolioPermission)
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
