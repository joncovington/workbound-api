from django.test import TestCase
from django.contrib.auth import get_user_model
from portfolio.models import Portfolio


class TestPortfolioModels(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@workbound.info',
            password='testpass123'
        )

    def test_create_portfolio(self):
        new_portfolio = Portfolio.objects.create(
            reference='TEST123',
            user=self.user
        )
        self.assertEqual(new_portfolio.reference, 'TEST123')
        self.assertEqual(new_portfolio.completed, False)
        self.assertIsNotNone(new_portfolio.created)

    def test_portfolio_str_representation(self):
        new_portfolio = Portfolio.objects.create(
            reference='TEST123',
            user=self.user
        )
        self.assertEqual(str(new_portfolio), new_portfolio.reference)
