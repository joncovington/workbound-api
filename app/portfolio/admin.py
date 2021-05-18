from django.contrib import admin
from portfolio.models import Portfolio, SectionCategory, Section


class PortfolioAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ['portfolio_id', 'reference', 'created', ]


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(SectionCategory)
admin.site.register(Section)
