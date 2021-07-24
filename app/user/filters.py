import django_filters
from user.models import Role


class RoleFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Role
        fields = ['category', ]
