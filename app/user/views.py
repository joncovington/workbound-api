from rest_framework import generics, authentication, permissions, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from user.models import Role

from user.serializers import UserSerializer, AuthTokenSerializer, RoleSerializer


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm(
                'user.view_role'
            )
        if request.method == 'POST':
            return request.user.has_perm(
                'user.add_role'
            )


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class RoleViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  ):
    """Manage Roles in the database"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, RolePermission)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleUserListView(generics.ListAPIView):
    """List roles for current user"""
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        user = self.request.user
        return Role.objects.filter(user=user)
