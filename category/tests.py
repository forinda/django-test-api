from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User
from .models import Category


class CategoryCRUDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        resp = self.client.post('/api/v1/categories/', {
            'name': 'Tech',
            'description': 'Technology articles',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_list_categories(self):
        Category.objects.create(name='Tech', description='Tech')
        resp = self.client.get('/api/v1/categories/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_retrieve_category_with_tasks(self):
        cat = Category.objects.create(name='Tech', description='Tech')
        resp = self.client.get(f'/api/v1/categories/{cat.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('tasks', resp.data)

    def test_update_category(self):
        cat = Category.objects.create(name='Tech', description='Tech')
        resp = self.client.patch(f'/api/v1/categories/{cat.pk}/', {'name': 'Science'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        cat.refresh_from_db()
        self.assertEqual(cat.name, 'Science')

    def test_delete_category(self):
        cat = Category.objects.create(name='Tech', description='Tech')
        resp = self.client.delete(f'/api/v1/categories/{cat.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
