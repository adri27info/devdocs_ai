from rest_framework import serializers

from apps.users_documents_feedbacks.models import UserDocumentFeedback


class UserDocumentFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocumentFeedback
        fields = "__all__"
