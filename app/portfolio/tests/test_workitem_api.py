import random
from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework.test import APIClient
from rest_framework import status

from utils.helpers import sample_email, sample_id

from portfolio.serializers import TaskSerializer, WorkItemSerializer
from portfolio.models import Task, WorkItem
from portfolio.tests.test_section_api import sample_section


User = get_user_model()

NO_PERMISSION = {
    'detail': 'You do not have permission to perform this action.'
}
WORKITEM_URL = reverse('portfolio:workitem-list')
TASK_URL = reverse('portfolio:task-list')


def _sample_user():
    return User.objects.create_user(email=sample_email(), password=sample_id())


def _get_user(**kwargs):
    """Return user from dict if present or return sample user"""
    user = kwargs['user'] if 'user' in kwargs else _sample_user()
    if not isinstance(user, User):
        raise ValueError(_('User must be an instance of AUTH_USER_MODEL'))
    return user


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

# Task tests

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
        self.assertEqual(res.data['results'], serializer.data)
        self.assertEqual(len(res.data['results']), len(task_qs))
        self.assertTrue(len(tasks))

    def test_retrieve_tasks_without_permission(self):
        """Test retrieving tasks without permissions"""

        tasks = [sample_task() for i in range(2)]

        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
        self.assertTrue(len(tasks))

    def test_create_task_with_permissions_successful(self):
        """Test creating new task successful with permissions"""
        payload = {
            'title': 'new_task',
            'description': 'blah blah blah',
            'duration': 1,
            'created_by': self.user.id,
            'completion_days': 7
        }
        permission = Permission.objects.get(name='Can add Task')
        self.user.user_permissions.add(permission)

        self.client.post(TASK_URL, payload)
        exists = Task.objects.filter(
            title=payload['title']
        ).exists()

        self.assertTrue(exists)

    def test_create_task_without_permissions_fails(self):
        """Test creating new task fails without permissions"""
        payload = {
            'title': 'new_task',
            'description': 'blah blah blah',
            'duration': 1,
            'completion_days': 7
        }

        res = self.client.post(TASK_URL, payload)

        exists = Task.objects.filter(
            title=payload['title']
        ).exists()

        self.assertFalse(exists)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)

# WorkItem tests

    def test_retrieve_workitem_with_permission_successful(self):
        """Test retrieving WorkItem(s) with correct permissions"""

        workitems = [sample_workitem() for i in range(2)]

        # add view permission for sections
        permission = Permission.objects.get(name='Can view Work Item')
        self.user.user_permissions.add(permission)

        res = self.client.get(WORKITEM_URL)

        workitem_qs = WorkItem.objects.all()
        serializer = WorkItemSerializer(workitem_qs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
        self.assertEqual(len(res.data['results']), len(workitem_qs))
        self.assertTrue(len(workitems))

    def test_retrieve_workitem_without_permission_fails(self):
        """Test retrieving WorkItem(s) without permissions fails"""

        workitems = [sample_workitem() for i in range(2)]

        res = self.client.get(WORKITEM_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
        self.assertTrue(len(workitems))

    def test_create_workitem_with_permission_successful(self):
        """Test creating new workitem successful"""
        section = sample_section()
        task = sample_task()

        payload = {
            'section': section.id,
            'task': task.id,
            'created_by': self.user.id
        }

        permission = Permission.objects.get(name='Can add Work Item')
        self.user.user_permissions.add(permission)

        res = self.client.post(WORKITEM_URL, payload)

        exists = WorkItem.objects.filter(
            section=section,
            task=task,
            created_by=self.user
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_workitem_without_permission_fails(self):
        """Test creating new workitem fails without permissions"""
        section = sample_section()
        task = sample_task()
        payload = {'section': section.id, 'task': task.id, 'created_by': self.user.id}

        res = self.client.post(WORKITEM_URL, payload)

        exists = WorkItem.objects.filter(
            section=section,
            task=task,
            created_by=self.user
        ).exists()

        self.assertFalse(exists)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, NO_PERMISSION)
