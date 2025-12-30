from django.urls import path

from apps.users.views.auth.login.login_user_view import LoginUserView
from apps.users.views.auth.register.register_user_view import RegisterUserView
from apps.users.views.auth.activate_account.activate_user_account_view import \
    ActivateUserAccountView
from apps.users.views.auth.resend_activation_code.resend_user_activation_code_view import (
    ResendUserActivationCodeView
)
from apps.users.views.auth.reset_password.reset_user_password_view import ResetUserPasswordView
from apps.users.views.auth.reset_password.reset_user_password_confirm_view import (
    ResetUserPasswordConfirmView
)
from apps.users.views.auth.tokens.refresh_token.refresh_token_custom_user_view import (
    RefreshTokenCustomUserView
)
from apps.users.views.auth.tokens.revoke.revoke_and_clear_tokens_user_view import (
    RevokeAndClearTokensUserView
)
from apps.users.views.auth.tokens.clear.clear_tokens_user_view import ClearTokensUserView
from apps.users.views.auth.tokens.csrf_token.csrf_token_user_view import CSRFTokenUserView
from apps.users.views.auth.assistance.assistance_user_view import AssistanceUserView


urlpatterns = [
    path("assistance/", AssistanceUserView.as_view(), name="assistance"),
    path("token/refresh/", RefreshTokenCustomUserView.as_view(), name="token_refresh"),
    path("token/revoke/", RevokeAndClearTokensUserView.as_view(), name="token_revoke"),
    path("token/force-logout/", ClearTokensUserView.as_view(), name="token_revoke_all"),
    path("token/csrf-refresh/", CSRFTokenUserView.as_view(), name="csrf_token_refresh"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path(
        "activate-user-account/",
        ActivateUserAccountView.as_view(),
        name="activate_user_account"
    ),
    path(
        "resend-user-activation-code/",
        ResendUserActivationCodeView.as_view(),
        name="resend_user_activation_code"
    ),
    path("reset-password/", ResetUserPasswordView.as_view(), name="reset_password"),
    path(
        "reset-password/confirm/",
        ResetUserPasswordConfirmView.as_view(),
        name="reset_password_confirm"
    ),
]
