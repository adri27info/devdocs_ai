from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("admin/", admin.site.urls),
    path("documents/", include("apps.documents.urls")),
    path("documents_contexts/", include("apps.documents_contexts.urls")),
    path("documents_feedbacks/", include("apps.documents_feedbacks.urls")),
    path("invoices/", include("apps.invoices.urls")),
    path("llm/", include("apps.llms.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("payments/", include("apps.payments.urls")),
    path("projects/", include("apps.projects.urls")),
    path("", include("apps.users.urls")),
]
