# from django.test import TestCase
# from django.contrib.auth.models import Permission
# from django.urls import reverse
# from django.contrib.auth import get_user_model

# from rest_framework.test import APIClient
# from rest_framework import status

# from portfolio.models import Portfolio, Section, SectionCategory

# NO_PERMISSION = {
#     'detail': 'You do not have permission to perform this action.'
# }
# SECTION_URL = reverse('portfolio:section-list')


# class PublicSectionApiTests(TestCase):
#     """Tests Section API (public)"""

#     def setUp(self) -> None:
#         self.client = APIClient()

#     def test_login_required(self):
#         """Test login required to use API"""
#         res = self.client.get(SECTION_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivatePortfolioApiTests(TestCase):
#     """Tests Portfolio API (private)"""

#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.user = get_user_model().objects.create(
#             email='test@workbound.info',
#             password='testpass123'
#         )
#         self.client.force_authenticate(user=self.user)

#         Portfolio.objects.create(
#             reference='TEST_Portfolio_123',
#             created_by=self.user,
#         )
