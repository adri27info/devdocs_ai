from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings

from .managers import UserManager

from utils.general_utils import GeneralUtils


def user_attachment_upload_to(instance, filename):
    """
    Generate a unique file path for user attachments using GeneralUtils.
    """
    return GeneralUtils.generate_attachment_path(
        instance=instance,
        filename=filename,
        folder="attachments/user",
        prefix="user"
    )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    attachment = models.FileField(
        upload_to=user_attachment_upload_to,
        default=settings.AWS_USER_IMAGE_BUCKET_URL,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    activation_code = models.CharField(max_length=5, blank=True, null=True)
    plan_type = models.ForeignKey(
        "plans_types.PlanType",
        related_name="users",
        on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        "roles.Role",
        related_name="users",
        on_delete=models.CASCADE
    )
    projects = models.ManyToManyField(
        "projects.Project",
        related_name="users",
        through="users_projects.UserProject",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
