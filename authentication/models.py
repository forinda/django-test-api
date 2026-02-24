from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class Permission(models.IntegerChoices):
    FOLLOW = 1, "Follow users"
    COMMENT = 2, "Comment on posts"
    WRITE = 4, "Write articles"
    MODERATE = 8, "Moderate comments"
    ADMIN = 16, "Administration access"


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    permissions = models.IntegerField(default=0)

    def has_permission(self, perm: Permission) -> bool:
        return bool(self.permissions & perm)

    def add_permission(self, perm: Permission):
        self.permissions |= perm

    def remove_permission(self, perm: Permission):
        self.permissions &= ~perm

    def reset_permissions(self):
        self.permissions = 0

    def get_permissions_list(self) -> list[str]:
        return [p.label for p in Permission if self.permissions & p]

    def __str__(self):
        return self.name

    @staticmethod
    def insert_roles():
        """Seed default roles."""
        roles = {
            'User': Permission.FOLLOW,
            'Moderator': (
                Permission.FOLLOW
                | Permission.COMMENT
                | Permission.WRITE
                | Permission.MODERATE
            ),
            'Administrator': (
                Permission.FOLLOW
                | Permission.COMMENT
                | Permission.WRITE
                | Permission.MODERATE
                | Permission.ADMIN
            ),
        }
        for name, perms in roles.items():
            role, _ = Role.objects.get_or_create(name=name)
            role.permissions = perms
            role.save()


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"
        OTHER = "Other", "Other"

    email = models.EmailField(unique=True)
    username = None
    gender = models.CharField(
        max_length=10, choices=Gender.choices, null=True, blank=True
    )
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users'
    )

    objects = UserManager()  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_app_permission(self, perm: Permission) -> bool:
        """Check if the user's role has a given permission."""
        if self.role is None:
            return False
        return self.role.has_permission(perm)

