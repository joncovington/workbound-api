from django.contrib import admin
from portfolio.models import Portfolio


class PortfolioAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['reference', 'created', ]


admin.site.register(Portfolio, PortfolioAdmin)
