from django.urls import path

from apps.documents_contexts.views import DocumentContextView


urlpatterns = [
    path("", DocumentContextView.as_view(), name="documents_contexts"),
]
