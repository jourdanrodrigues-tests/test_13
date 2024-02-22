import csv
import io
from uuid import uuid4

from rest_framework.test import APITestCase

from app.factories import ConsumerFactory
from app.models import Consumer
from app.tests.utils import TestCaseMixin


class TestPost(TestCaseMixin, APITestCase):
    def test_that_it_returns_expected_response(self):
        client_ref = str(uuid4())
        csv_file = io.StringIO()
        csv.writer(csv_file).writerows(
            [
                ["ssn", "client reference no", "consumer name", "consumer address", "balance", "status"],
                ["123-45-6789", client_ref, "Jane Doe", "123 Main St", "1000", Consumer.StatusChoices.IN_COLLECTION],
            ]
        )
        csv_file.seek(0)

        response = self.client.post("/consumers/upload_csv/", {"file": csv_file}, format="multipart")

        expected_data = [
            {
                "address": "123 Main St",
                "balance": 1000.0,
                "client_ref_number": client_ref,
                "name": "Jane Doe",
                "status": Consumer.StatusChoices.IN_COLLECTION,
            },
        ]
        self.assertOkResponse(response, expected_data)

    def test_when_consumer_does_not_exist_then_creates_it(self):
        ssn = "123-45-6789"
        client_ref = str(uuid4())
        csv_file = io.StringIO()
        csv.writer(csv_file).writerows(
            [
                ["ssn", "client reference no", "consumer name", "consumer address", "balance", "status"],
                [ssn, client_ref, "Jane Doe", "123 Main St", "1000", Consumer.StatusChoices.IN_COLLECTION],
                [ssn, client_ref, "Jane Doe", "123 Main St", "1020", Consumer.StatusChoices.PAID_IN_FULL],
            ]
        )
        csv_file.seek(0)

        self.client.post("/consumers/upload_csv/", {"file": csv_file}, format="multipart")

        queryset = Consumer.objects.filter(
            ssn=ssn,
            client_ref_number=client_ref,
            name="Jane Doe",
            balance=1020.0,
            status=Consumer.StatusChoices.PAID_IN_FULL,
            address="123 Main St",
        )
        self.assertTrue(queryset.exists())

    def test_when_there_are_multiple_entries_then_correctly_updates_the_consumer(self):
        consumer = ConsumerFactory()
        csv_file = io.StringIO()
        csv.writer(csv_file).writerows(
            [
                ["ssn", "client reference no", "consumer name", "consumer address", "balance", "status"],
                [
                    consumer.ssn,
                    consumer.client_ref_number,
                    consumer.name,
                    consumer.address,
                    str(consumer.balance),
                    consumer.status,
                ],
                [
                    consumer.ssn,
                    consumer.client_ref_number,
                    consumer.name,
                    consumer.address,
                    str(consumer.balance + 20),
                    Consumer.StatusChoices.INACTIVE,
                ],
                [
                    consumer.ssn,
                    consumer.client_ref_number,
                    consumer.name,
                    consumer.address,
                    str(consumer.balance + 10),
                    Consumer.StatusChoices.IN_COLLECTION,
                ],
                [
                    consumer.ssn,
                    consumer.client_ref_number,
                    consumer.name,
                    consumer.address,
                    str(consumer.balance + 30),
                    Consumer.StatusChoices.PAID_IN_FULL,
                ],
            ]
        )
        csv_file.seek(0)

        self.client.post("/consumers/upload_csv/", {"file": csv_file}, format="multipart")

        expected_balance = consumer.balance + 30
        consumer.refresh_from_db()
        self.assertListEqual(
            [consumer.balance, consumer.status],
            [expected_balance, Consumer.StatusChoices.PAID_IN_FULL],
        )

    def test_that_it_performs_expected_amount_of_queries(self):
        consumer = ConsumerFactory()
        csv_file = io.StringIO()
        csv.writer(csv_file).writerows(
            [
                ["ssn", "client reference no", "consumer name", "consumer address", "balance", "status"],
                [
                    consumer.ssn,
                    consumer.client_ref_number,
                    consumer.name,
                    consumer.address,
                    str(consumer.balance),
                    consumer.status,
                ],
                ["123-45-6789", str(uuid4()), "Cool Name", "1 Cool Street", "2", Consumer.StatusChoices.INACTIVE],
                ["123-45-6789", str(uuid4()), "Cool Name", "1 Cool Street", "500", Consumer.StatusChoices.PAID_IN_FULL],
                [
                    consumer.ssn,
                    consumer.client_ref_number,
                    consumer.name,
                    consumer.address,
                    str(consumer.balance + 30),
                    Consumer.StatusChoices.IN_COLLECTION,
                ],
            ]
        )
        csv_file.seek(0)

        with self.assertNumQueries(5):
            """
            Captured queries were:
            1. SAVEPOINT "s140150754138888_x2"
            2. SELECT "app_consumer"."ssn", "app_consumer"."client_ref_number", "app_consumer"."name", "app_consumer"."balance", "app_consumer"."status", "app_consumer"."address", "app_consumer"."created_date" FROM "app_consumer" WHERE "app_consumer"."ssn" IN ('325-58-2568', '123-45-6789')
            3. INSERT INTO "app_consumer" ("ssn", "client_ref_number", "name", "balance", "status", "address", "created_date") VALUES ('123-45-6789', '3d13ab8b-1fc9-43fd-8ffd-baaaefffc7d1'::uuid, 'Cool Name', 500.0, 'PAID_IN_FULL', '1 Cool Street', '2024-02-21T15:24:12.797534+00:00'::timestamptz)
            4. UPDATE "app_consumer" SET "balance" = (CASE WHEN ("app_consumer"."ssn" = '325-58-2568') THEN 962.0 WHEN ("app_consumer"."ssn" = '123-45-6789') THEN 500.0 ELSE NULL END)::double precision, "status" = (CASE WHEN ("app_consumer"."ssn" = '325-58-2568') THEN 'IN_COLLECTION' WHEN ("app_consumer"."ssn" = '123-45-6789') THEN 'PAID_IN_FULL' ELSE NULL END)::varchar(13), "client_ref_number" = (CAST(CASE WHEN ("app_consumer"."ssn" = '325-58-2568') THEN 'c31d50ac-bb42-46e4-b351-e4357cf8d21c'::uuid WHEN ("app_consumer"."ssn" = '123-45-6789') THEN '3d13ab8b-1fc9-43fd-8ffd-baaaefffc7d1'::uuid ELSE NULL END AS uuid))::uuid, "name" = (CASE WHEN ("app_consumer"."ssn" = '325-58-2568') THEN 'Consumer 0' WHEN ("app_consumer"."ssn" = '123-45-6789') THEN 'Cool Name' ELSE NULL END)::varchar(255), "address" = (CASE WHEN ("app_consumer"."ssn" = '325-58-2568') THEN 'PSC 4887, Box 3493 APO AP 01800' WHEN ("app_consumer"."ssn" = '123-45-6789') THEN '1 Cool Street' ELSE NULL END)::varchar(255) WHERE "app_consumer"."ssn" IN ('325-58-2568', '123-45-6789')
            5. RELEASE SAVEPOINT "s140150754138888_x2"
            """
            self.client.post("/consumers/upload_csv/", {"file": csv_file}, format="multipart")
