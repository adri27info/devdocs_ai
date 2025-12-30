from django.db.models import Avg

from rest_framework import serializers

from apps.documents.models import Document
from apps.documents_feedbacks.models import DocumentFeedback
from apps.users_documents_feedbacks.models import UserDocumentFeedback


class DocumentSerializer(serializers.ModelSerializer):
    user_attachment = serializers.SerializerMethodField()
    average_stars = serializers.SerializerMethodField()
    voted_user_ids = serializers.SerializerMethodField()

    class Meta:
        model = Document
        exclude = ["user"]

    def get_user_attachment(self, obj):
        user = obj.user
        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(user.attachment.url)

        return user.attachment.url

    def get_average_stars(self, obj):
        avg = DocumentFeedback.objects.filter(
            document=obj
        ).aggregate(avg=Avg("rating"))["avg"]

        return round(avg) if avg else 0

    def get_voted_user_ids(self, obj):
        voted_users = UserDocumentFeedback.objects.filter(
            document_feedback__document=obj,
            has_voted=True
        ).values_list("user_id", flat=True)

        return list(voted_users)
