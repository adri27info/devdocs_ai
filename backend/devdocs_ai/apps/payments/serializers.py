from rest_framework import serializers


class StripePaymentStatusSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True)

    def validate_session_id(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Stripe session_id cannot be empty")

        return value
