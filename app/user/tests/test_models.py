from django.test import TestCase
from django.contrib.auth import get_user_model

from portfolio.models import Category

from user.models import RoleType, Role


class TestUserModels(TestCase):
    """Test User Models"""

    def test_existing_role_types(self):
        """Test that default role types exist"""
        role_types = RoleType.objects.all()
        user_type_exists = RoleType.objects.filter(name='User').exists()
        manager_type_exists = RoleType.objects.filter(name='Manager').exists()

        self.assertTrue(user_type_exists)
        self.assertTrue(manager_type_exists)
        self.assertGreaterEqual(len(role_types), 2)

    def test_add_user_to_role(self):
        """Test adding user to a role within a category"""
        user = get_user_model().objects.create_user('test@workbound.info', 'testpass123')
        department = Category.objects.create(title='Test department', description='', created_by=user)
        role_type = RoleType.objects.get(name='User')
        Role.objects.create(user=user, category=department, role_type=role_type)
        test_role = Role.objects.filter(user=user)

        self.assertEqual(len(test_role), 1)
