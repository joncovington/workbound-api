from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.auth import get_user_model as User
from django.utils.translation import ugettext_lazy as _

from rest_framework.test import APIClient
from rest_framework import status

from utils.helpers import sample_email, sample_id
from portfolio.tests.test_portfolio_api import sample_portfolio

from portfolio.models import SectionCategory, Section
from portfolio.serializers import SectionSerializer


NO_PERMISSION = {
    'detail': 'You do not have permission to perform this action.'
}
SECTION_URL = reverse('portfolio:section-list')


def _sample_user():
    return User().objects.create(email=sample_email(), password=sample_id())


def _get_user(**kwargs):
    """Return user from dict if present or return sample user"""
    user = kwargs['user'] if 'user' in kwargs else _sample_user()
    if not isinstance(user, User()):
        raise ValueError(_('User must be an instance of AUTH_USER_MODEL'))
    return user


def sample_sectioncategory(*args, **kwargs):
    """Returns a sample SectionCategory object for testing"""
    user = _get_user(**kwargs)

    return SectionCategory.objects.create(
        title=sample_id(),
        description='',
        created_by=user
    )


def sample_section(*args, **kwargs):
    """Create and return a sample portfolio for testing"""
    user = _get_user(**kwargs)

    return Section.objects.create(
        portfolio=sample_portfolio(),
        category=sample_sectioncategory(),
        created_by=user
    )


class PublicSectionApiTests(TestCase):
    """Tests Section API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login required to use API"""
        res = self.client.get(SECTION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSectionApiTests(TestCase):
    """Tests Section API (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = _sample_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_sections_with_permission(self):
        """Test retrieving sections with correct permissions"""

        sections = [sample_section() for i in range(2)]

        # add view permission for sections
        permission = Permission.objects.get(name='Can view section')
        self.user.user_permissions.add(permission)

        res = self.client.get(SECTION_URL)

        section_qs = Section.objects.all()
        serializer = SectionSerializer(section_qs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), len(section_qs))
        self.assertTrue(len(sections))
