from rest_framework import generics, permissions, viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from user.models import Role

from user.serializers import UserSerializer, RoleSerializer

def get_perm_by_model_name(name, user):
    perms = list(x.replace('portfolio.', '') for x in user.get_all_permissions() if x.endswith(f'_{name}'))
    return perms

@api_view(['GET', ])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def custom_user_model_permissions(request):
    print(request.data)
    task_perms = get_perm_by_model_name(name=request.data['perm'], user=request.user)

    return Response(status=status.HTTP_200_OK, data={'task_permissions': task_perms})

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


class BlacklistTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(self.serializer_class(user).data)

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
