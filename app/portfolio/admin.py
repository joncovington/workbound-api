from django.contrib import admin
from django.contrib.auth.models import Permission
from portfolio.models import Portfolio, Category, Section, Task, WorkItem


admin.site.register(Permission)


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ('portfolio_id', 'reference', 'created', 'section_count')
    readonly_fields = ('portfolio_id', 'created', 'completed')

    def section_count(self, obj):
        return obj.sections.count()

    section_count.short_description = 'sections'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ('title', 'created', 'archived')
    readonly_fields = ('created', 'archived')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ('section_id', 'created', 'workitem_count')
    readonly_fields = ('section_id', 'created', 'completed')

    def workitem_count(self, obj):
        return obj.workitems.count()

    workitem_count.short_description = 'Work Items'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ('title', 'created', 'archived')
    readonly_fields = ('created', 'archived')


@admin.register(WorkItem)
class WorkItemAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ('workitem_id', 'created', 'assigned_to', )
    readonly_fields = ('workitem_id', 'created', 'completed')
