from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='super@workbound.info',
            password='superpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@workbound.info',
            password='pass123'
        )

    def test_users_listed(self):
        """Test users are listed in admin user page"""
        url = reverse('admin:core_customuser_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user change page works"""
        url = reverse('admin:core_customuser_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_add_page(self):
        """Test that user add page works"""
        url = reverse('admin:core_customuser_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
