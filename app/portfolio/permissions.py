from django.utils.translation import ugettext_lazy as _

from rest_framework.permissions import BasePermission, DjangoModelPermissions

from user.models import Role, RoleType


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """Overridde DjangoModelPermissions to require view permissions"""
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class IsAssigned(BasePermission):
    """
    Object-level permission to only allow assigned user of an object to edit it.
    """
    message = _('You must be assigned to this object.')

    def has_object_permission(self, request, view, obj):

        check_role = Role.objects.filter(
            user=request.user,
            category=obj.section.category,
            role_type=RoleType.objects.get(name='Manager')
        )

        return obj.assigned_to == request.user or check_role
