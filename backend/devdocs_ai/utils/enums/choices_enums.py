from django.db import models


class DocumentationFormatEnum(models.TextChoices):
    PLAIN = 'plain', 'Plain Text'
    PDF = 'pdf', 'PDF'


class SubscriptionPlanEnum(models.TextChoices):
    FREE = 'free', 'Free'
    PREMIUM = 'premium', 'Premium'


class NotificationTypeEnum(models.TextChoices):
    INFO = 'info', 'Info'
    RESET = 'reset', 'Reset'
    ACTION_REQUIRED = 'action_required', 'Action Required'


class ResetReasonEnum(models.TextChoices):
    RESET_ACTIVATION_ATTEMPTS = "reset_activation_code_attempts", "Reset activation code attempts"
    RESET_PASSWORD_ATTEMPTS = "reset_password_attempts", "Reset password attempts"


class ActionRequiredReasonEnum(models.TextChoices):
    PROJECT_INVITATION = "project_invitation", "Project invitation"
    DOC_SUGGESTION = "doc_suggestion", "Doc suggestion"


class PrivacyEnum(models.TextChoices):
    PUBLIC = 'public', 'Public'
    PRIVATE = 'private', 'Private'


class RoleEnum(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'


class RoleProjectEnum(models.TextChoices):
    OWNER = 'owner', 'Owner'
    MEMBER = 'member', 'Member'
