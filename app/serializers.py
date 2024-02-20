from rest_framework import serializers

from app.models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    ssn = serializers.CharField(max_length=9, write_only=True)  # I think this is extremely sensitive

    class Meta:
        model = Consumer
        fields = ("ssn", "client_ref_number", "name", "balance", "status")
