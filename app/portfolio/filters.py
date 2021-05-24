import django_filters
from portfolio.models import SectionCategory, Task, WorkItem


class TaskFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ('title', )


class SectionCategoryFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = SectionCategory
        fields = ('title', )


class WorkItemFilter(django_filters.FilterSet):

    assigned_to__email = django_filters.CharFilter(lookup_expr='icontains')
    completed = django_filters.BooleanFilter()

    class Meta:
        model = WorkItem
        fields = ('assigned_to', )
