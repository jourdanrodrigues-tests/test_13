import csv

import io
import re

from django.db import transaction
from rest_framework import serializers

from app.models import Consumer


class ConsumerDataSerializer(serializers.Serializer):
    balance = serializers.FloatField()
    status = serializers.CharField(max_length=13)
    ssn = serializers.CharField(max_length=11)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Really couldn't think of a better way and I didn't want to install Pydantic
        self.fields["client reference no"] = serializers.UUIDField(source="client_ref_number")
        self.fields["consumer name"] = serializers.CharField(max_length=255, source="name")
        self.fields["consumer address"] = serializers.CharField(max_length=255, source="address")

    @staticmethod
    def validate_ssn(value: str) -> str:
        if not re.match(r'^(\d{3}-\d{2}-\d{4}|\d{9})$', value):
            raise serializers.ValidationError("SSN must be 9 or 11 characters long")
        return value if '-' in value else f"{value[:3]}-{value[3:5]}-{value[5:]}"

    class Meta:
        fields = ("ssn", "client reference no", "consumer name", "balance", "status", "consumer address")


class ConsumerSerializer(serializers.ModelSerializer):
    ssn = serializers.CharField(max_length=9, write_only=True)  # I think this is extremely sensitive

    class Meta:
        model = Consumer
        fields = ("ssn", "client_ref_number", "name", "balance", "status", "address")


class ConsumerCsvUploadSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True)
    consumers = serializers.ListField(child=ConsumerSerializer(), read_only=True)

    @staticmethod
    def validate_file(file) -> list[dict]:
        output = []
        for row in csv.DictReader(io.TextIOWrapper(file, encoding='utf-8')):
            serializer = ConsumerDataSerializer(data=row)
            serializer.is_valid(raise_exception=True)
            output.append(serializer.validated_data)
        return output

    class Meta:
        model = Consumer
        fields = ("file", "consumers")

    @transaction.atomic
    def create(self, validated_data: dict) -> dict:
        entries = validated_data['file']
        consumers = self._fetch_consumers(entries)

        consumer_lookup = {consumer.ssn: consumer for consumer in consumers}

        for entry in entries:
            consumer = consumer_lookup[entry['ssn']]
            for field, value in entry.items():
                setattr(consumer, field, value)

        fields = [field for field in entries[0].keys() if field != Consumer._meta.pk.name]
        Consumer.objects.bulk_update(consumers, fields=fields)

        return {'consumers': ConsumerSerializer(consumers, many=True).data}

    @staticmethod
    def _fetch_consumers(entries: list[dict]) -> list[Consumer]:
        ssn_lookup = {entry["ssn"]: entry for entry in entries}
        ssns_sent = ssn_lookup.keys()

        consumers_found = list(Consumer.objects.filter(ssn__in=ssns_sent))
        missing_ssns = list(set(ssns_sent).difference(consumer.ssn for consumer in consumers_found))

        new_consumers = Consumer.objects.bulk_create([Consumer(**ssn_lookup[ssn]) for ssn in missing_ssns])

        return consumers_found + new_consumers

