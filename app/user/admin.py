from django.contrib import admin

from user.models import RoleType, Role


class RoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'role_type']


class RoleTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']


admin.site.register(Role, RoleAdmin)
admin.site.register(RoleType, RoleTypeAdmin)
