from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User, Role, Permission
from category.models import Category
from .models import Article


def make_writer():
    role = Role.objects.create(
        name='writer',
        permissions=Permission.FOLLOW | Permission.COMMENT | Permission.WRITE,
    )
    return User.objects.create_user(email='writer@example.com', password='testpass123', role=role)


def make_reader():
    role = Role.objects.create(name='reader', permissions=Permission.FOLLOW)
    return User.objects.create_user(email='reader@example.com', password='testpass123', role=role)


class ArticleCRUDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.writer = make_writer()
        self.client.force_authenticate(user=self.writer)
        self.category = Category.objects.create(name='Tech', description='Tech articles')

    def test_create_article(self):
        resp = self.client.post('/api/v1/articles/', {
            'title': 'Test Article',
            'slug': 'test-article',
            'body': 'Article body content',
            'status': 'Draft',
            'category': self.category.pk,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().author, self.writer)

    def test_list_articles(self):
        Article.objects.create(
            title='A1', slug='a1', body='body', author=self.writer, category=self.category,
        )
        resp = self.client.get('/api/v1/articles/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertIn('likes_count', resp.data[0])
        self.assertIn('comments_count', resp.data[0])
        self.assertIn('is_liked', resp.data[0])

    def test_retrieve_article(self):
        article = Article.objects.create(
            title='A1', slug='a1', body='body', author=self.writer,
        )
        resp = self.client.get(f'/api/v1/articles/{article.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['title'], 'A1')

    def test_update_article(self):
        article = Article.objects.create(
            title='A1', slug='a1', body='body', author=self.writer,
        )
        resp = self.client.patch(f'/api/v1/articles/{article.pk}/', {'title': 'Updated'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        article.refresh_from_db()
        self.assertEqual(article.title, 'Updated')

    def test_delete_article(self):
        article = Article.objects.create(
            title='A1', slug='a1', body='body', author=self.writer,
        )
        resp = self.client.delete(f'/api/v1/articles/{article.pk}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)


class ArticlePermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.reader = make_reader()

    def test_reader_cannot_create(self):
        self.client.force_authenticate(user=self.reader)
        resp = self.client.post('/api/v1/articles/', {
            'title': 'Test', 'slug': 'test', 'body': 'body',
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_can_list(self):
        self.client.force_authenticate(user=self.reader)
        resp = self.client.get('/api/v1/articles/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthenticated_rejected(self):
        resp = self.client.get('/api/v1/articles/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class ArticleSearchFilterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.writer = make_writer()
        self.client.force_authenticate(user=self.writer)
        self.cat = Category.objects.create(name='Tech', description='Tech')
        Article.objects.create(
            title='Django Tips', slug='django-tips', body='Learn Django',
            author=self.writer, category=self.cat, status='Published',
        )
        Article.objects.create(
            title='React Guide', slug='react-guide', body='Learn React',
            author=self.writer, status='Draft',
        )

    def test_search_by_title(self):
        resp = self.client.get('/api/v1/articles/', {'search': 'Django'})
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['title'], 'Django Tips')

    def test_filter_by_status(self):
        resp = self.client.get('/api/v1/articles/', {'status': 'Published'})
        self.assertEqual(len(resp.data), 1)

    def test_filter_by_category(self):
        resp = self.client.get('/api/v1/articles/', {'category': self.cat.pk})
        self.assertEqual(len(resp.data), 1)

    def test_ordering(self):
        resp = self.client.get('/api/v1/articles/', {'ordering': 'title'})
        titles = [a['title'] for a in resp.data]
        self.assertEqual(titles, sorted(titles))
