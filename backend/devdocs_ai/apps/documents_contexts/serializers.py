from rest_framework import serializers

from apps.documents_contexts.models import DocumentContext

from utils.exceptions.db.db_exceptions import DatabaseOperationException
from utils.validators.document_context.create.document_context_create_validator \
    import DocumentContextCreateValidator


class DocumentContextCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentContext
        fields = "__all__"
        extra_kwargs = {
            'body_prompt': {
                'error_messages': {
                    'required': 'Body prompt is required.',
                    'blank': 'Body prompt may not be blank.'
                }
            },
            'project': {
                'error_messages': {
                    'required': 'Project is required.',
                    'null': 'Project may not be null.'
                }
            },
            'format': {
                'error_messages': {
                    'required': 'Format is required.',
                    'null': 'Format may not be null.'
                }
            },
            "llm": {
                "required": False
            },
        }

    def validate_body_prompt(self, value):
        return value.strip()

    def validate(self, data):
        data["llm"] = DocumentContextCreateValidator.run(
            request_user=self.context['request'].user,
            data=data,
        )

        return data

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Exception:
            raise DatabaseOperationException(
                "Document context could not be created."
            )
