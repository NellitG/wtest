from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = "__all__"
        read_only_fields = ["id", "date", "receipt_number"]

    def create(self, validated_data):
        prev = validated_data["previous_reading"]
        curr = validated_data["current_reading"]
        rate = validated_data["rate_per_unit"]

        validated_data["units_consumed"] = curr - prev
        validated_data["amount"] = validated_data["units_consumed"] * rate

        validated_data["receipt_number"] = "RCP-" + get_random_string(8).upper()

        return super().create(validated_data)