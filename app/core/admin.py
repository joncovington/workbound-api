from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', ]
    fieldsets = (
        (None, {'fields': ('email', 'password', 'firebase_uid')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['view_user_email', 'first_name', 'last_name']

    def view_user_email(self, obj):
        return obj.user.email


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.CustomUser, UserAdmin)
