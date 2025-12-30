from django.urls import path

from apps.documents.views import DocumentView


urlpatterns = [
    path("", DocumentView.as_view(), name="documents"),
]
