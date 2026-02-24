from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User, Role, Permission


def make_admin():
    role = Role.objects.create(
        name='admin',
        permissions=Permission.FOLLOW | Permission.COMMENT | Permission.WRITE | Permission.MODERATE | Permission.ADMIN,
    )
    return User.objects.create_user(email='admin@example.com', password='testpass123', role=role)


def make_regular_user():
    role = Role.objects.create(name='regular', permissions=Permission.FOLLOW)
    return User.objects.create_user(email='regular@example.com', password='testpass123', role=role)


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = make_admin()
        self.client.force_authenticate(user=self.admin)

    def test_list_users(self):
        resp = self.client.get('/api/v1/users/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        resp = self.client.post('/api/v1/users/', {
            'email': 'newuser@example.com',
            'password': 'securepass123',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_retrieve_user(self):
        user = User.objects.create_user(email='target@example.com', password='testpass123')
        resp = self.client.get(f'/api/v1/users/{user.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['email'], 'target@example.com')

    def test_update_user(self):
        user = User.objects.create_user(email='target@example.com', password='testpass123')
        resp = self.client.patch(f'/api/v1/users/{user.pk}/', {'first_name': 'John'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'John')

    def test_delete_user(self):
        user = User.objects.create_user(email='target@example.com', password='testpass123')
        resp = self.client.delete(f'/api/v1/users/{user.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class UserViewSetPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_non_admin_cannot_list(self):
        regular = make_regular_user()
        self.client.force_authenticate(user=regular)
        resp = self.client.get('/api/v1/users/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_rejected(self):
        resp = self.client.get('/api/v1/users/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class RoleViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = make_admin()
        self.client.force_authenticate(user=self.admin)

    def test_list_roles(self):
        resp = self.client.get('/api/v1/users/roles/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_role(self):
        role = Role.objects.create(name='TestRole', permissions=Permission.FOLLOW)
        resp = self.client.get(f'/api/v1/users/roles/{role.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('permissions_list', resp.data)

    def test_create_not_allowed(self):
        resp = self.client.post('/api/v1/users/roles/', {
            'name': 'Editor',
            'permissions': Permission.FOLLOW | Permission.WRITE,
        })
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed(self):
        role = Role.objects.create(name='TestRole', permissions=0)
        resp = self.client.delete(f'/api/v1/users/roles/{role.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_any_authenticated_user_can_list(self):
        regular = make_regular_user()
        self.client.force_authenticate(user=regular)
        resp = self.client.get('/api/v1/users/roles/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthenticated_rejected(self):
        self.client.force_authenticate(user=None)
        resp = self.client.get('/api/v1/users/roles/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
