from django.contrib import admin

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from apps.users.models import User

admin.site.register(User)
admin.site.unregister(OutstandingToken)


@admin.register(OutstandingToken)
class CustomOutstandingTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "jti", "token", "created_at", "expires_at")

    def has_delete_permission(self, request, obj=None):
        return True
