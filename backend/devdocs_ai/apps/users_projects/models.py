from django.db import models


class UserProject(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE
    )
    role_project = models.ForeignKey(
        "roles_projects.RoleProject",
        related_name="users_projects",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User project"
        verbose_name_plural = "Users projects"
