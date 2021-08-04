from django.contrib.auth.models import Permission
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from portfolio.models import Category
from user.models import Role, RoleType
from user.serializers import RoleSerializer

User = get_user_model()

NO_PERMISSION = {
    'detail': 'You do not have permission to perform this action.'
}
ROLE_URL = reverse('user:role-list')
USER_ROLE_URL = reverse('user:my_roles')


class PublicRoleApiTests(TestCase):
    """Tests Roles API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login required to use API"""
        res = self.client.get(ROLE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_required_my_roles(self):
        """Test login required to get request user roles"""
        res = self.client.get(USER_ROLE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRoleApiTests(TestCase):
    """Tests Role API (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@workbound.info',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        Category.objects.create(title='department', description='', created_by=self.user)

    def test_retrieve_roles_with_permissions(self):
        """Test retrieving roles while user has permissions"""
        permission = Permission.objects.get(name='Can view role')
        self.user.user_permissions.add(permission)

        Role.objects.create(
            user=self.user,
            category=Category.objects.create(title='department 1',
                                             description='',
                                             created_by=self.user
                                             ),
            role_type=RoleType.objects.first()
        )
        Role.objects.create(
            user=User.objects.create_user(email='another@workbound.info',
                                          password='testpass222',
                                          ),
            category=Category.objects.create(title='department 2',
                                             description='',
                                             created_by=self.user,
                                             ),
            role_type=RoleType.objects.last()
        )

        res = self.client.get(ROLE_URL)

        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
        self.assertEqual(len(res.data['results']), 2)

    def test_retrieve_roles_without_permissions(self):
        """Test retrieving roles while user doesn't have permissions"""
        Role.objects.create(
            user=self.user,
            category=Category.objects.create(title='department 1',
                                             description='',
                                             created_by=self.user
                                             ),
            role_type=RoleType.objects.first()
        )
        Role.objects.create(
            user=User.objects.create_user(email='another@workbound.info',
                                          password='testpass222',
                                          ),
            category=Category.objects.create(title='department 2',
                                             description='',
                                             created_by=self.user,
                                             ),
            role_type=RoleType.objects.last()
        )

        res = self.client.get(ROLE_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)

    def test_create_role_successful_with_permission(self):
        """Test creating new role successful when user has permission"""
        user = User.objects.create_user(
            email='another@workbound.info',
            password='testpass222',
        )
        category = Category.objects.create(
            title='department 1',
            description='sfasdf',
            created_by=self.user,
        )
        role_type = RoleType.objects.first()
        payload = {'user': user.id, 'category': category.id, 'role_type': role_type.id}

        permission = Permission.objects.get(name='Can add role')
        self.user.user_permissions.add(permission)

        res = self.client.post(ROLE_URL, payload)
        exists = Role.objects.filter(
            user=user,
            category=category,
            role_type=role_type
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_role_fails_without_permission(self):
        """Test creating new role fails when user doesn't have permission"""
        user = User.objects.create_user(
            email='another@workbound.info',
            password='testpass222',
        )
        category = Category.objects.create(
            title='department 1',
            description='asdfasdf',
            created_by=self.user,
        )
        role_type = RoleType.objects.first()
        payload = {'user': user.id, 'category': category.id, 'role_type': role_type.id}

        res = self.client.post(ROLE_URL, payload)
        exists = Role.objects.filter(
            user=user,
            category=category,
            role_type=role_type
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
        self.assertFalse(exists)
