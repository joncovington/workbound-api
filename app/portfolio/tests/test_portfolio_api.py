import json
import random
from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework.test import APIClient
from rest_framework import status

from portfolio.models import Portfolio, Task, Category
from portfolio.serializers import PortfolioSerializer

from utils.helpers import sample_id, sample_email


User = get_user_model()

NO_PERMISSION = {
    'detail': 'You do not have permission to perform this action.'
}
PORTFOLIO_URL = reverse('portfolio:portfolio-list')


def _sample_user():
    return User.objects.create_user(email=sample_email(), password=sample_id())


def _get_user(**kwargs):
    """Return user from dict if present or return sample user"""
    user = kwargs['user'] if 'user' in kwargs else _sample_user()
    if not isinstance(user, User):
        raise ValueError(_('User must be an instance of AUTH_USER_MODEL'))
    return user


def sample_portfolio(**kwargs) -> Portfolio:
    """Create and return a sample portfolio for testing"""
    user = _get_user(**kwargs)
    return Portfolio.objects.create(
        reference=sample_id(),
        created_by=user,
    )


def sample_task(*args, **kwargs):
    """Returns a sample Task object for testing"""
    user = _get_user(**kwargs)

    return Task.objects.create(
        title=sample_id(),
        description='',
        created_by=user,
        duration=1,
        completion_days=random.randint(1, 14)
    )


def sample_category(*args, **kwargs):
    """Returns a sample Category object for testing"""
    user = _get_user(**kwargs)

    return Category.objects.create(
        title=sample_id(),
        description='',
        created_by=user
    )


class PublicPortfolioApiTests(TestCase):
    """Tests Portfolio API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login required to use API"""
        res = self.client.get(PORTFOLIO_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivatePortfolioApiTests(TestCase):
    """Tests Portfolio API (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = _sample_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_portfolios_with_permission(self):
        """Test retrieving portfolios with correct permissions"""

        portfolios = [sample_portfolio() for i in range(2)]

        # add view permission for portfolios
        permission = Permission.objects.get(name='Can view Portfolio')
        self.user.user_permissions.add(permission)

        res = self.client.get(PORTFOLIO_URL)

        portfolios_qs = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios_qs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
        self.assertTrue(len(portfolios))
        self.assertEqual(len(res.data['results']), len(portfolios_qs))

    def test_retrieve_portfolios_without_permission(self):
        """Test retrieving portfolios without correct permissions"""
        permission = Permission.objects.get(name='Can view Portfolio')
        self.user.user_permissions.remove(permission.id)
        portfolios = [sample_portfolio() for i in range(2)]

        res = self.client.get(PORTFOLIO_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
        self.assertTrue(len(portfolios))

    def test_create_portfolio_successful(self):
        """Test creating new portfolio successful"""
        payload = {'reference': 'BrandNewPortfolio-000', 'created_by': self.user.id}

        permission = Permission.objects.get(name='Can add Portfolio')
        self.user.user_permissions.add(permission)

        self.client.post(PORTFOLIO_URL, payload)
        exists = Portfolio.objects.filter(
            reference=payload['reference']
        ).exists()

        self.assertTrue(exists)

    def test_create_portfolio_invalid_permissions(self):
        """Test creating new portfolio with invalid permissions"""
        payload = {'reference': 'BrandNewPortfolio-000', 'user': self.user.id}

        res = self.client.post(PORTFOLIO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_portfolio_successful_with_metadata(self):
        """Test creating new portfolio successful with metadata"""
        meta = {'firstkey': 'firstvalue', 'secondkey': 'secondvalue'}

        payload = {
            'reference': 'BrandNewPortfolio-000',
            'created_by': self.user.id,
            'meta': json.dumps(meta)
        }

        permission = Permission.objects.get(name='Can add Portfolio')
        self.user.user_permissions.add(permission)

        res = self.client.post(PORTFOLIO_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['meta'], meta)
