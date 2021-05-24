from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.auth import get_user_model as User
from django.utils.translation import ugettext_lazy as _

from rest_framework.test import APIClient
from rest_framework import status
from portfolio.serializers import TaskSerializer

from utils.helpers import sample_email, sample_id

from portfolio.models import Task, WorkItem
from portfolio.tests.test_section_api import sample_section

NO_PERMISSION = {
    'detail': 'You do not have permission to perform this action.'
}
# WORKITEM_URL = reverse('portfolio:workitem-list')
TASK_URL = reverse('portfolio:task-list')


def _sample_user():
    return User().objects.create(email=sample_email(), password=sample_id())


def _get_user(**kwargs):
    """Return user from dict if present or return sample user"""
    user = kwargs['user'] if 'user' in kwargs else _sample_user()
    if not isinstance(user, User()):
        raise ValueError(_('User must be an instance of AUTH_USER_MODEL'))
    return user


def sample_task(*args, **kwargs):
    """Returns a sample Task object for testing"""
    user = _get_user(**kwargs)

    return Task.objects.create(
        title=sample_id(),
        description='',
        created_by=user,
        duration=1
    )


def sample_workitem(*args, **kwargs):
    """Returns a sample WorkItem object for testing"""
    user = _get_user(**kwargs)

    return WorkItem.objects.create(
        section=sample_section(),
        task=sample_task(),
        created_by=user
    )


class PublicWorkItemApiTests(TestCase):
    """Tests WorkItem API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login required to use API"""
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorkItemApiTests(TestCase):
    """Tests WorkItem API (private)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = _sample_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tasks_with_permission(self):
        """Test retrieving tasks with correct permissions"""

        tasks = [sample_task() for i in range(2)]

        # add view permission for tasks
        permission = Permission.objects.get(name='Can view Task')
        self.user.user_permissions.add(permission)

        res = self.client.get(TASK_URL)

        task_qs = Task.objects.all()
        serializer = TaskSerializer(task_qs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), len(task_qs))
        self.assertTrue(len(tasks))

    def test_retrieve_tasks_without_permission(self):
        """Test retrieving tasks without permissions"""

        tasks = [sample_task() for i in range(2)]

        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
        self.assertTrue(len(tasks))

    def test_create_task_successful(self):
        """Test creating new task successful"""
        payload = {
            'title': 'new_task',
            'description': 'blah blah blah',
            'duration': 1
        }

        permission = Permission.objects.get(name='Can add Task')
        self.user.user_permissions.add(permission)

        self.client.post(TASK_URL, payload)
        exists = Task.objects.filter(
            title=payload['title']
        ).exists()

        self.assertTrue(exists)