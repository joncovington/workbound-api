from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from firebase_admin import auth


CREATE_USER_URL = reverse('user:create')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test user API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@workbound.info',
            'password': 'testpass123'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(id=res.data['id'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        firebase_user = auth.get_user_by_email(user.email)
        auth.delete_user(firebase_user.uid)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@workbound.info',
            'password': 'testpass123'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password must be more than 5 characters"""
        payload = {
            'email': 'test@workbound.info',
            'password': '123'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self) -> None:
        self.user = create_user(
            email='test@workbound.info',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], self.user.id)
        self.assertEqual(res.data['email'], self.user.email)

    def test_post_me_not_allowed(self):
        """Test POST not allowed for ME endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(
            res.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_update_user_password(self):
        """Test updating password for authenticated user"""
        payload = {'password': 'new|password'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
