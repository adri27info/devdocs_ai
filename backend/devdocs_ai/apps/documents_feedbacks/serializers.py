from rest_framework import serializers

from apps.documents_feedbacks.models import DocumentFeedback
from apps.users_documents_feedbacks.models import UserDocumentFeedback

from utils.exceptions.db.db_exceptions import DatabaseOperationException


class DocumentFeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFeedback
        fields = "__all__"
        extra_kwargs = {
            'document': {
                'error_messages': {
                    'required': 'Document is required.',
                    'null': 'Document may not be null.'
                }
            },
            'rating': {
                'error_messages': {
                    'required': 'Rating is required.',
                    'null': 'Rating may not be null.',
                    'invalid': 'Rating must be a valid integer.'
                }
            },
        }

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            feedback = super().create(validated_data)

            UserDocumentFeedback.objects.create(
                user=user,
                document_feedback=feedback,
                has_voted=True
            )

            return feedback
        except Exception:
            raise DatabaseOperationException(
                "Document feedback could not be created."
            )
