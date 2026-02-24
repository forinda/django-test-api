from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User, Role, Permission
from articles.models import Article
from .models import Comment


def make_commenter():
    role = Role.objects.create(
        name="commenter",
        permissions=Permission.FOLLOW | Permission.COMMENT | Permission.WRITE,
    )
    return User.objects.create_user(
        email="commenter@example.com", password="testpass123", role=role
    )


def make_moderator():
    role = Role.objects.create(
        name="moderator",
        permissions=Permission.FOLLOW
        | Permission.COMMENT
        | Permission.WRITE
        | Permission.MODERATE,
    )
    return User.objects.create_user(
        email="mod@example.com", password="testpass123", role=role
    )


def make_reader():
    role = Role.objects.create(name="reader", permissions=Permission.FOLLOW)
    return User.objects.create_user(
        email="reader@example.com", password="testpass123", role=role
    )


class CommentCRUDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_commenter()
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(
            title="Test",
            slug="test",
            body="body",
            author=self.user,
        )

    def test_create_comment(self):
        resp = self.client.post(
            "/api/v1/comments/",
            {
                "article": self.article.pk,
                "body": "Great article!",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.user)

    def test_list_comments(self):
        Comment.objects.create(article=self.article, author=self.user, body="Comment 1")
        resp = self.client.get("/api/v1/comments/", {"article": self.article.pk})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_update_own_comment(self):
        comment = Comment.objects.create(
            article=self.article, author=self.user, body="Old"
        )
        resp = self.client.patch(f"/api/v1/comments/{comment.pk}/", {"body": "Updated"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.body, "Updated")

    def test_delete_own_comment(self):
        comment = Comment.objects.create(
            article=self.article, author=self.user, body="Delete me"
        )
        resp = self.client.delete(f"/api/v1/comments/{comment.pk}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class ThreadedCommentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_commenter()
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(
            title="Test",
            slug="test",
            body="body",
            author=self.user,
        )

    def test_create_reply(self):
        parent = Comment.objects.create(
            article=self.article, author=self.user, body="Parent"
        )
        resp = self.client.post(
            "/api/v1/comments/",
            {
                "article": self.article.pk,
                "body": "Reply",
                "parent": parent.pk,
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_replies_nested_in_list(self):
        parent = Comment.objects.create(
            article=self.article, author=self.user, body="Parent"
        )
        Comment.objects.create(
            article=self.article, author=self.user, body="Reply", parent=parent
        )
        resp = self.client.get("/api/v1/comments/", {"article": self.article.pk})
        # Only top-level comments in list
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(len(resp.data[0]["replies"]), 1)


class CommentPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.commenter = make_commenter()
        self.article = Article.objects.create(
            title="Test",
            slug="test",
            body="body",
            author=self.commenter,
        )

    def test_reader_cannot_create_comment(self):
        reader = make_reader()
        self.client.force_authenticate(user=reader)
        resp = self.client.post(
            "/api/v1/comments/",
            {
                "article": self.article.pk,
                "body": "Nope",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_can_list_comments(self):
        reader = make_reader()
        self.client.force_authenticate(user=reader)
        resp = self.client.get("/api/v1/comments/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_cannot_edit_others_comment(self):
        other = User.objects.create_user(
            email="other@example.com", password="testpass123", role=self.commenter.role
        )
        comment = Comment.objects.create(
            article=self.article, author=self.commenter, body="Mine"
        )
        self.client.force_authenticate(user=other)
        resp = self.client.patch(f"/api/v1/comments/{comment.pk}/", {"body": "Hacked"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_delete_others_comment(self):
        mod = make_moderator()
        comment = Comment.objects.create(
            article=self.article, author=self.commenter, body="Delete me"
        )
        self.client.force_authenticate(user=mod)
        resp = self.client.delete(f"/api/v1/comments/{comment.pk}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
