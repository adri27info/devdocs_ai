from django.utils import timezone

from rest_framework import serializers

from apps.documents_contexts.models import DocumentContext
from apps.llms.models import LLM


class DocumentContextCreateValidator:
    """
    Validator for creating DocumentContext instances.

    Ensures that:
        - The user's plan permits the requested output format.
        - The related LLM can process the prompt length.
        - The LLM has sufficient remaining daily tokens.
        - The project does not exceed the maximum allowed document contexts.

    Updates the LLM's daily token usage accordingly.
    """
    __CHARS_PER_TOKEN = 4
    __MAX_DOCUMENTS_CONTEXS_PER_PROJECT = 5

    @classmethod
    def run(cls, *, request_user, data):
        """
        Validate a DocumentContext creation request.

        This method performs multiple checks:
            1. Ensures an LLM exists.
            2. Limits the number of DocumentContext per project.
            3. Checks user plan restrictions for output format.
            4. Validates the prompt length against the LLM's per-request limit.
            5. Validates the daily token usage for the LLM and updates it.

        Args:
            request_user (User): The user creating the DocumentContext.
            data (dict): Dictionary containing:
                - "body_prompt" (str): Text to be processed by the LLM.
                - "format" (Format): Requested output format for the document.
                - "project" (Project): Related project instance.

        Returns:
            LLM: The LLM instance after updating daily token usage.

        Raises:
            serializers.ValidationError: Raised in the following cases:
                - No LLM exists.
                - Project has reached max document contexts.
                - User's plan does not allow requested format.
                - Prompt exceeds the LLM's per-request token limit.
                - LLM's daily token limit exceeded.
        """
        llm = LLM.objects.first()

        if not llm:
            raise serializers.ValidationError(
                {
                    "detail": "LLM does not exist."
                }
            )

        project = data["project"]
        existing_contexts_count = DocumentContext.objects.filter(project=project).count()

        if existing_contexts_count >= cls.__MAX_DOCUMENTS_CONTEXS_PER_PROJECT:
            raise serializers.ValidationError(
                {
                    "detail": (
                        f"This project already has the maximum of "
                        f"{cls.__MAX_DOCUMENTS_CONTEXS_PER_PROJECT} document contexts."
                    )
                }
            )

        format = data["format"]
        body_prompt = data["body_prompt"]

        if request_user.plan_type.name == "free" and format.name == "pdf":
            raise serializers.ValidationError(
                {
                    "detail": "Your plan does not allow converting documents to PDF."
                }
            )

        estimated_tokens = len(body_prompt) // cls.__CHARS_PER_TOKEN

        if estimated_tokens > llm.max_tokens_per_request:
            raise serializers.ValidationError(
                {
                    "detail": "Prompt is too long for this LLM."
                }
            )

        if llm.tokens_per_day_last_reset.date() < timezone.now().date():
            llm.tokens_per_day_used_today = 0
            llm.tokens_per_day_last_reset = timezone.now()
            llm.save(update_fields=["tokens_per_day_used_today", "tokens_per_day_last_reset"])

        if llm.tokens_per_day_used_today + estimated_tokens > llm.max_tokens_per_day:
            raise serializers.ValidationError(
                {
                    "detail": "LLM daily token limit exceeded."
                }
            )

        llm.tokens_per_day_used_today += estimated_tokens
        llm.save(update_fields=["tokens_per_day_used_today"])

        return llm
