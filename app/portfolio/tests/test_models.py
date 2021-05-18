from django.test import TestCase
from django.contrib.auth import get_user_model
from portfolio.models import Portfolio, SectionCategory, Section


class TestPortfolioModels(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@workbound.info',
            password='testpass123'
        )

    def test_create_portfolio(self):
        new_portfolio = Portfolio.objects.create(
            reference='TEST123',
            created_by=self.user
        )
        self.assertEqual(new_portfolio.reference, 'TEST123')
        self.assertEqual(bool(new_portfolio.completed), False)
        self.assertIsNotNone(new_portfolio.created)

    def test_portfolio_str_representation(self):
        new_portfolio = Portfolio.objects.create(
            reference='TEST123',
            created_by=self.user
        )
        self.assertEqual(str(new_portfolio), new_portfolio.portfolio_id)


class TestSectionModels(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@workbound.info',
            password='testpass123'
        )

    def test_section_category_str(self):
        """Test Section Category __str__"""
        sectioncategory = SectionCategory.objects.create(
            name='Section Category One',
            description='Test description goes here',
            created_by=self.user
        )

        self.assertEqual(bool(sectioncategory.archived), False)
        self.assertIsNotNone(sectioncategory.created)
        self.assertEqual(str(sectioncategory), sectioncategory.name)

    def test_section_str(self):
        """Test Section __str__"""
        new_portfolio = Portfolio.objects.create(
            reference='TEST123',
            created_by=self.user
        )
        sectioncategory = SectionCategory.objects.create(
            name='Section Category One',
            description='Test description goes here',
            created_by=self.user
        )
        section = Section.objects.create(
            category=sectioncategory,
            portfolio=new_portfolio,
            created_by=self.user
        )

        self.assertEqual(bool(section.completed), False)
        self.assertIsNotNone(section.created)
        self.assertEqual(str(section), f'{section.section_id} {sectioncategory.name}')
