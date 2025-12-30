from django.urls import path

from apps.users_documents_feedbacks.views import UserDocumentFeedbackView

urlpatterns = [
    path("", UserDocumentFeedbackView.as_view(), name="users_documents_feedbacks"),
]
