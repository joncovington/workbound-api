import secrets
import requests
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import generics, permissions, viewsets, mixins, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from auth.authentication import FirebaseAuthentication
from user.filters import RoleFilter
from user.models import Role

from user.serializers import ProfileSerializer, UserSerializer, RoleSerializer

from firebase_admin import auth

User = get_user_model()


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


@api_view(['POST', ])
def verify_recaptcha(request):
    """Custom view to validate recaptchaV2 token"""
    token = request.data['recaptcha']
    print(token)
    print(settings.RECAPTCHA_SECRET_KEY)
    print(request.META.get('HTTP_X_FORWARDED_FOR'))
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token,
        # 'remoteip': request.META.get('HTTP_X_FORWARDED_FOR'),
        'remoteip': 'localhost'
    }
    try:
        response = requests.post(url=recaptcha_url, data=payload)
        result = response.json()
        success = result.get('success', False)
        if success:
            return Response(status=status.HTTP_200_OK, data={'detail': 'reCaptcha verified'})
    except requests.exceptions.RequestException as err:
        print('recaptcha fail')
        return Response(status=status.HTTP_403_FORBIDDEN, data={'errors': err})
    return Response(status=status.HTTP_403_FORBIDDEN)


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


@api_view(['POST', ])
def sync_firebase_user(request):
    """Custom view to sync a firebase user to our user table"""
    print('Syncing firebase_user')
    print(request.data)
    if request.method == 'POST':
        if not request.data['token']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                decoded_token = auth.verify_id_token(request.data['token'])
                email = decoded_token['email']
                uid = decoded_token['uid']
            except auth.UserNotFoundError:
                return Response(data={'error': 'User Not Found'}, status=status.HTTP_401_UNAUTHORIZED)

            if len(User.objects.filter(email=email)) == 0:
                new_django_user = User.objects.create(email=email, password=secrets.token_urlsafe())
                new_django_user.firebase_uid = uid
                new_django_user.save()
                serialzer = UserSerializer(instance=new_django_user).data
                return Response(data=serialzer, status=status.HTTP_200_OK)
            else:
                existing_user = User.objects.get(email=email)
                if existing_user.firebase_uid == uid:
                    return Response(status=status.HTTP_200_OK)
                else:
                    existing_user.firebase_uid = uid
                    existing_user.save()
                    return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


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
    authentication_classes = (FirebaseAuthentication, )

    def get_queryset(self):
        user = self.request.user
        return Role.objects.filter(user=user)
