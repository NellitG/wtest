from rest_framework import serializers
from .models import MeterReading

class MeterReadingSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.name')

    class Meta:
        model = MeterReading
        fields = [
            'id', 'client', 'client_name', 'meter_number',
            'current_reading', 'previous_reading',
            'units_consumed', 'rate_per_unit', 'receipt_number',  'amount', 'date'
        ]
        read_only_fields = ['previous_reading', 'units_consumed', 'amount']

    def create(self, validated_data):
        client = validated_data['client']
        current_reading = validated_data['current_reading']

        # Get the last reading for this client
        last = MeterReading.objects.filter(client=client).order_by('-date').first()
        prev = last.current_reading if last else 0

        # Validation check
        if current_reading < prev:
            raise serializers.ValidationError("Current reading cannot be less than previous reading.")

        # Compute billing values
        validated_data['previous_reading'] = prev
        validated_data['units_consumed'] = current_reading - prev
        validated_data['amount'] = validated_data['units_consumed'] * MeterReading.RATE_PER_UNIT

        return super().create(validated_data)

    def update(self, instance, validated_data):
        client = validated_data.get('client', instance.client)
        current_reading = validated_data.get('current_reading', instance.current_reading)

        last = MeterReading.objects.filter(client=client).order_by('-date').first()
        prev = last.current_reading if last else 0

        if current_reading < prev:
            raise serializers.ValidationError("Current reading cannot be less than previous reading.")

        validated_data['previous_reading'] = prev
        validated_data['units_consumed'] = current_reading - prev
        validated_data['amount'] = validated_data['units_consumed'] * MeterReading.RATE_PER_UNIT

        return super().update(instance, validated_data)