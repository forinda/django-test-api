from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Role, Permission


class RoleModelTest(TestCase):
    def test_has_permission(self):
        role = Role.objects.create(name='test', permissions=Permission.FOLLOW | Permission.WRITE)
        self.assertTrue(role.has_permission(Permission.FOLLOW))
        self.assertTrue(role.has_permission(Permission.WRITE))
        self.assertFalse(role.has_permission(Permission.ADMIN))

    def test_add_and_remove_permission(self):
        role = Role.objects.create(name='test', permissions=0)
        role.add_permission(Permission.COMMENT)
        self.assertTrue(role.has_permission(Permission.COMMENT))
        role.remove_permission(Permission.COMMENT)
        self.assertFalse(role.has_permission(Permission.COMMENT))

    def test_reset_permissions(self):
        role = Role.objects.create(name='test', permissions=31)
        role.reset_permissions()
        self.assertEqual(role.permissions, 0)

    def test_get_permissions_list(self):
        role = Role.objects.create(name='test', permissions=Permission.FOLLOW | Permission.COMMENT)
        labels = role.get_permissions_list()
        self.assertIn('Follow users', labels)
        self.assertIn('Comment on posts', labels)

    def test_insert_roles(self):
        Role.insert_roles()
        self.assertEqual(Role.objects.count(), 3)
        self.assertTrue(Role.objects.filter(name='User').exists())
        self.assertTrue(Role.objects.filter(name='Moderator').exists())
        self.assertTrue(Role.objects.filter(name='Administrator').exists())


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)

    def test_create_user_no_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpass123')

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='admin@example.com', password='adminpass123')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_has_app_permission_no_role(self):
        user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.assertFalse(user.has_app_permission(Permission.FOLLOW))

    def test_has_app_permission_with_role(self):
        role = Role.objects.create(name='writer', permissions=Permission.WRITE)
        user = User.objects.create_user(email='test@example.com', password='testpass123', role=role)
        self.assertTrue(user.has_app_permission(Permission.WRITE))
        self.assertFalse(user.has_app_permission(Permission.ADMIN))


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        resp = self.client.post('/api/v1/auth/register/', {
            'email': 'new@example.com',
            'password': 'securepass123',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

    def test_register_short_password(self):
        resp = self.client.post('/api/v1/auth/register/', {
            'email': 'new@example.com',
            'password': 'short',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        User.objects.create_user(email='dup@example.com', password='testpass123')
        resp = self.client.post('/api/v1/auth/register/', {
            'email': 'dup@example.com',
            'password': 'securepass123',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')

    def test_login_success(self):
        resp = self.client.post('/api/v1/auth/login/', {
            'email': 'user@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)
        self.assertIn('user', resp.data)

    def test_login_wrong_password(self):
        resp = self.client.post('/api/v1/auth/login/', {
            'email': 'user@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        resp = self.client.post('/api/v1/auth/login/', {
            'email': 'nobody@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenRefreshTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')

    def test_refresh_token(self):
        login_resp = self.client.post('/api/v1/auth/login/', {
            'email': 'user@example.com',
            'password': 'testpass123',
        })
        refresh = login_resp.data['refresh']
        resp = self.client.post('/api/v1/auth/refresh/', {'refresh': refresh})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        resp = self.client.get('/api/v1/auth/profile/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['email'], 'user@example.com')

    def test_patch_profile(self):
        resp = self.client.patch('/api/v1/auth/profile/', {'gender': 'Male'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.gender, 'Male')

    def test_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        resp = self.client.get('/api/v1/auth/profile/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='oldpass123')
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        resp = self.client.post('/api/v1/auth/change-password/', {
            'old_password': 'oldpass123',
            'new_password': 'newpass1234',
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass1234'))

    def test_change_password_wrong_old(self):
        resp = self.client.post('/api/v1/auth/change-password/', {
            'old_password': 'wrongold',
            'new_password': 'newpass1234',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class ForgotResetPasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')

    def test_forgot_password(self):
        resp = self.client.post('/api/v1/auth/forgot-password/', {'email': 'user@example.com'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('uid', resp.data)
        self.assertIn('token', resp.data)

    def test_forgot_password_nonexistent_email(self):
        resp = self.client.post('/api/v1/auth/forgot-password/', {'email': 'nobody@example.com'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        forgot_resp = self.client.post('/api/v1/auth/forgot-password/', {'email': 'user@example.com'})
        resp = self.client.post('/api/v1/auth/reset-password/', {
            'uid': forgot_resp.data['uid'],
            'token': forgot_resp.data['token'],
            'new_password': 'resetpass123',
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('resetpass123'))

    def test_reset_password_invalid_token(self):
        forgot_resp = self.client.post('/api/v1/auth/forgot-password/', {'email': 'user@example.com'})
        resp = self.client.post('/api/v1/auth/reset-password/', {
            'uid': forgot_resp.data['uid'],
            'token': 'invalid-token',
            'new_password': 'resetpass123',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
