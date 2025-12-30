from django.urls import path

from apps.documents_feedbacks.views import DocumentFeedbackView


urlpatterns = [
    path("", DocumentFeedbackView.as_view(), name="documents_feedbacks"),
]
