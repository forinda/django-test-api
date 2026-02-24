from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from category.models import Category
from .models import Task


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Work', description='Work tasks')

    def test_create_task(self):
        resp = self.client.post('/api/v1/tasks/', {
            'title': 'My Task',
            'description': 'Task description',
            'category': self.category.pk,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_list_tasks(self):
        Task.objects.create(title='T1', description='D1', category=self.category)
        resp = self.client.get('/api/v1/tasks/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_retrieve_task(self):
        task = Task.objects.create(title='T1', description='D1')
        resp = self.client.get(f'/api/v1/tasks/{task.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['title'], 'T1')

    def test_update_task(self):
        task = Task.objects.create(title='T1', description='D1')
        resp = self.client.patch(f'/api/v1/tasks/{task.pk}/', {'title': 'Updated'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated')

    def test_delete_task(self):
        task = Task.objects.create(title='T1', description='D1')
        resp = self.client.delete(f'/api/v1/tasks/{task.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_complete_task(self):
        task = Task.objects.create(title='T1', description='D1', completed=False)
        resp = self.client.patch(f'/api/v1/tasks/{task.pk}/', {'completed': True})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertTrue(task.completed)
