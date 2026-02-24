from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User, Role, Permission
from articles.models import Article
from .models import Like


def make_user(email="user@example.com"):
    role, _ = Role.objects.get_or_create(
        name="basic",
        defaults={
            "permissions": Permission.FOLLOW | Permission.COMMENT | Permission.WRITE
        },
    )
    return User.objects.create_user(email=email, password="testpass123", role=role)


class LikeCRUDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(
            title="Test",
            slug="test",
            body="body",
            author=self.user,
        )

    def test_like_article(self):
        resp = self.client.post("/api/v1/likes/", {"article": self.article.pk})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_article(self):
        like = Like.objects.create(article=self.article, user=self.user)
        resp = self.client.delete(f"/api/v1/likes/{like.pk}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_duplicate_like_rejected(self):
        self.client.post("/api/v1/likes/", {"article": self.article.pk})
        resp = self.client.post("/api/v1/likes/", {"article": self.article.pk})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_likes_for_article(self):
        Like.objects.create(article=self.article, user=self.user)
        resp = self.client.get("/api/v1/likes/", {"article": self.article.pk})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_unauthenticated_rejected(self):
        self.client.force_authenticate(user=None)
        resp = self.client.post("/api/v1/likes/", {"article": self.article.pk})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_put_patch_allowed(self):
        like = Like.objects.create(article=self.article, user=self.user)
        resp = self.client.put(
            f"/api/v1/likes/{like.pk}/", {"article": self.article.pk}
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        resp = self.client.patch(
            f"/api/v1/likes/{like.pk}/", {"article": self.article.pk}
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
