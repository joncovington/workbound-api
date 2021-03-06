from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework.test import APIClient
from rest_framework import status

from utils.helpers import sample_email, sample_id
from portfolio.tests.test_portfolio_api import sample_portfolio

from portfolio.models import Category, Section
from portfolio.serializers import SectionSerializer, CategorySerializer


User = get_user_model()

NO_PERMISSION = {"detail": "You do not have permission to perform this action."}
SECTION_URL = reverse("portfolio:section-list")
SECTIONCATEGORY_URL = reverse("portfolio:category-list")


def _sample_user():
    return User.objects.create_user(email=sample_email(), password=sample_id())


def _get_user(**kwargs):
    """Return user from dict if present or return sample user"""
    user = kwargs["user"] if "user" in kwargs else _sample_user()
    if not isinstance(user, User):
        raise ValueError(_("User must be an instance of AUTH_USER_MODEL"))
    return user


def sample_category(*args, **kwargs):
    """Returns a sample Category object for testing"""
    user = _get_user(**kwargs)

    return Category.objects.create(title=sample_id(), description="", created_by=user)


def sample_section(*args, **kwargs):
    """Create and return a sample portfolio for testing"""
    user = _get_user(**kwargs)

    return Section.objects.create(
        portfolio=sample_portfolio(), category=sample_category(), created_by=user
    )


class PublicSectionApiTests(TestCase):
    """Tests Section API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login required to use API"""
        res = self.client.get(SECTION_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateSectionApiTests(TestCase):
    """Tests Section API (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = _sample_user()
        self.client.force_authenticate(user=self.user)

    # Category Tests

    def test_retrieve_category_with_permission(self):
        """Test retrieving sections with correct permissions"""

        categories = [sample_category() for i in range(2)]

        # add view permission for category
        permission = Permission.objects.get(name="Can view Category")
        self.user.user_permissions.add(permission)

        res = self.client.get(SECTIONCATEGORY_URL)

        sectioncat_qs = Category.objects.all()
        serializer = CategorySerializer(sectioncat_qs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(len(res.data["results"]), len(sectioncat_qs))
        self.assertTrue(len(categories))

    def test_retrieve_category_without_permissions(self):
        """Test retrieving sections without permissions"""
        permission = Permission.objects.get(name='Can view Category')
        self.user.user_permissions.remove(permission.id)
        categories = [sample_category() for i in range(2)]

        res = self.client.get(SECTIONCATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
        self.assertTrue(len(categories))

    def test_create_category_successful(self):
        """Test creating new category successful"""
        payload = {
            "title": "new_category",
            "description": "blah blah blah",
            "created_by": self.user.id,
        }

        permission = Permission.objects.get(name="Can add Category")
        self.user.user_permissions.add(permission)

        self.client.post(SECTIONCATEGORY_URL, payload)
        exists = Category.objects.filter(title=payload["title"]).exists()

        self.assertTrue(exists)

    def test_create_category_without_permission_fails(self):
        """Test creating new category without permissions fails"""
        payload = {"title": "new_category", "description": "blah blah blah"}

        res = self.client.post(SECTIONCATEGORY_URL, payload)

        exists = Category.objects.filter(title=payload["title"]).exists()

        self.assertFalse(exists)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)

    # Section tests

    def test_retrieve_sections_with_permission(self):
        """Test retrieving sections with correct permissions"""

        sections = [sample_section() for i in range(2)]

        # add view permission for sections
        permission = Permission.objects.get(name="Can view Section")
        self.user.user_permissions.add(permission)

        res = self.client.get(SECTION_URL)

        section_qs = Section.objects.all()
        serializer = SectionSerializer(section_qs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(len(res.data["results"]), len(section_qs))
        self.assertTrue(len(sections))

    def test_retrieve_section_without_permissions(self):
        """Test retrieving sections without permissions"""
        permission = Permission.objects.get(name='Can view Section')
        self.user.user_permissions.remove(permission.id)
        sections = [sample_section() for i in range(2)]

        res = self.client.get(SECTION_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
        self.assertTrue(len(sections))

    def test_create_section_with_permission_successful(self):
        """Test creating new section successful"""
        portfolio = sample_portfolio()
        category = sample_category()
        payload = {
            "portfolio": portfolio.id,
            "category": category.id,
            "created_by": self.user.id,
        }

        permission = Permission.objects.get(name="Can add Section")
        self.user.user_permissions.add(permission)

        res = self.client.post(SECTION_URL, payload)

        exists = Section.objects.filter(
            portfolio=portfolio, category=category, created_by=self.user
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_section_without_permission_fails(self):
        """Test creating new section without pemission fails"""
        portfolio = sample_portfolio()
        category = sample_category()
        payload = {
            "portfolio": portfolio.id,
            "category": category.id,
            "created_by": self.user.id,
        }

        res = self.client.post(SECTION_URL, payload)

        exists = Section.objects.filter(
            portfolio=portfolio, category=category, created_by=self.user
        ).exists()

        self.assertFalse(exists)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
