from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """Overridde DjangoModelPermissions to require view permissions"""
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
