from rest_framework.generics import GenericAPIView

from apps.users_documents_feedbacks.models import UserDocumentFeedback
from apps.users_documents_feedbacks.serializers import UserDocumentFeedbackSerializer


class UserDocumentFeedbackView(GenericAPIView):
    serializer_class = UserDocumentFeedbackSerializer

    def get_queryset(self):
        return UserDocumentFeedback.objects.all()
