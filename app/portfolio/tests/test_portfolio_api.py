from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from portfolio.models import Portfolio
from portfolio.serializers import PortfolioSerializer

NO_PERMISSION = {
    'detail': 'You do not have permission to perform this action.'
}
PORTFOLIO_URL = reverse('portfolio:portfolio-list')


class PublicPortfolioApiTests(TestCase):
    """Tests Portfolio API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login required to use API"""
        res = self.client.get(PORTFOLIO_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePortfolioApiTests(TestCase):
    """Tests Portfolio API (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='test@workbound.info',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_portfolios_with_permission(self):
        """Test retrieving portfolios with correct permissions"""
        Portfolio.objects.create(
            reference='TEST_Portfolio_123',
            user=self.user,
        )
        Portfolio.objects.create(
            reference='Second_PORTFOLIO|777',
            user=self.user,
        )
        # add view permission for portfolios
        permission = Permission.objects.get(name='Can view portfolio')
        self.user.user_permissions.add(permission)

        res = self.client.get(PORTFOLIO_URL)

        portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_retrieve_portfolios_without_permission(self):
        """Test retrieving portfolios without correct permissions"""
        Portfolio.objects.create(
            reference='TEST_Portfolio_123',
            user=self.user,
        )
        Portfolio.objects.create(
            reference='Second_PORTFOLIO|777',
            user=self.user,
        )

        res = self.client.get(PORTFOLIO_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], NO_PERMISSION['detail'])

    def test_create_portfolio_successful(self):
        """Test creating new portfolio successful"""
        payload = {'reference': 'BrandNewPortfolio-000', 'user': self.user.id}

        permission = Permission.objects.get(name='Can add portfolio')
        self.user.user_permissions.add(permission)

        self.client.post(PORTFOLIO_URL, payload)
        exists = Portfolio.objects.filter(
            reference=payload['reference']
        ).exists()

        self.assertTrue(exists)

    def test_create_portfolio_invalid(self):
        """Test creating new portfolio with invalid data"""
        payload = {'reference': '', 'user': self.user.id}

        permission = Permission.objects.get(name='Can add portfolio')
        self.user.user_permissions.add(permission)

        res = self.client.post(PORTFOLIO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
