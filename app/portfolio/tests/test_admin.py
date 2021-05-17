from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from portfolio.models import Portfolio


class TestPortfolioAdmin(TestCase):
    """Test Portfolio Admin"""
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='super@workbound.info',
            password='superpass123'
        )
        self.user = get_user_model().objects.create_user(
            email='test@workbound.info',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        self.portfolio = Portfolio.objects.create(
            reference='TEST123',
            user=self.user
        )

    def test_portfolios_listed(self):
        """Test portfolios are listed in admin portfolio page"""
        url = reverse('admin:portfolio_portfolio_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.portfolio.reference)
