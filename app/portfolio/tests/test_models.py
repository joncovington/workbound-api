from django.test import TestCase
from portfolio.models import Portfolio


class TestPortfolioModels(TestCase):

    def test_create_portfolio(self):
        new_portfolio = Portfolio.objects.create(
            reference='TEST123'
        )
        self.assertEqual(new_portfolio.reference, 'TEST123')
        self.assertEqual(new_portfolio.completed, False)
        self.assertIsNotNone(new_portfolio.created)

    def test_portfolio_str_representation(self):
        new_portfolio = Portfolio.objects.create(
            reference='TEST123'
        )
        self.assertEqual(str(new_portfolio), new_portfolio.reference)
