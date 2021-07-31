from django.contrib.auth.models import Permission
from rest_framework import generics, permissions, viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from auth.authentication import FirebaseAuthentication
from user.filters import RoleFilter
from user.models import Role

from user.serializers import ProfileSerializer, UserSerializer, RoleSerializer


def get_perm_by_model_name(name, user):
    perms = list(x.replace('portfolio.', '') for x in user.get_all_permissions() if x.endswith(f'_{name}'))
    perms.sort()
    perm_names = [{'verbose': x.name, 'status': True} for x in Permission.objects.filter(codename__in=perms)]
    return (dict(zip(perms, perm_names)))


@api_view(['GET', ])
@authentication_classes([FirebaseAuthentication])
@permission_classes([permissions.IsAuthenticated])
def custom_user_model_permissions(request, model):
    perms = get_perm_by_model_name(name=model, user=request.user)

    return Response(status=status.HTTP_200_OK, data={f'{model}_permissions': perms})


@api_view(['GET', ])
@authentication_classes([FirebaseAuthentication])
@permission_classes([permissions.IsAuthenticated])
def retrieve_all_permissions(request):
    all_perms = []
    models = ['task', 'category', 'workitem', 'section', 'portfolio']
    for model in models:
        perms = get_perm_by_model_name(name=model, user=request.user)
        all_perms.append({model: perms})
    return Response(status=status.HTTP_200_OK, data=all_perms)


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


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(self.serializer_class(user).data)


class ProfileView(generics.UpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = ProfileSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        try:
            serializer.is_valid()
            serializer.save()
            response_data = UserSerializer(instance=self.request.user).data
            return Response(response_data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"errors": (serializer.errors,)},
                            status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  ):
    """Manage Roles in the database"""
    authentication_classes = (FirebaseAuthentication, )
    permission_classes = (permissions.IsAuthenticated, RolePermission)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_class = RoleFilter


class RoleUserListView(generics.ListAPIView):
    """List roles for current user"""
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        user = self.request.user
        return Role.objects.filter(user=user)
