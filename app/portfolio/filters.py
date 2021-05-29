import django_filters
from django_filters.widgets import DateRangeWidget
from portfolio.models import Category, Portfolio, Section, Task, WorkItem


class TaskFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ('title', )


class CategoryFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ('title', )


class WorkItemFilter(django_filters.FilterSet):

    assigned_to__email = django_filters.CharFilter(lookup_expr='icontains')
    assigned_to__id = django_filters.CharFilter(lookup_expr='exact')
    created = django_filters.DateFromToRangeFilter(widget=DateRangeWidget(attrs={'type': 'date'}))
    completed = django_filters.DateFromToRangeFilter(widget=DateRangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = WorkItem
        fields = ('assigned_to', 'created', 'completed')


class SectionFilter(django_filters.FilterSet):

    workitems__assigned_to__email = django_filters.CharFilter(lookup_expr='icontains')
    workitems__assigned_to__id = django_filters.CharFilter(lookup_expr='exact')
    section_id = django_filters.CharFilter(lookup_expr='exact')
    created = django_filters.DateFromToRangeFilter(widget=DateRangeWidget(attrs={'type': 'date'}))
    completed = django_filters.DateFromToRangeFilter(widget=DateRangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Section
        fields = ('section_id', )


class PortfolioFilter(django_filters.FilterSet):

    sections__workitems__assigned_to__email = django_filters.CharFilter(lookup_expr='icontains')
    sections__workitems__assigned_to__id = django_filters.CharFilter(lookup_expr='exact')
    portfolio_id = django_filters.CharFilter(lookup_expr='exact')
    created = django_filters.DateFromToRangeFilter(widget=DateRangeWidget(attrs={'type': 'date'}))
    completed = django_filters.DateFromToRangeFilter(widget=DateRangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Portfolio
        fields = ('portfolio_id', )
