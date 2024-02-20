from rest_framework.test import APITestCase

from app.factories import ConsumerFactory
from app.tests.utils import TestCaseMixin


class TestGet(TestCaseMixin, APITestCase):
    def test_that_it_returns_expected_response(self):
        consumer = ConsumerFactory()

        response = self.client.get("/consumers/")

        expected_payload = {
            'next': None,
            'previous': None,
            'results': [
                {
                    "client_ref_number": str(consumer.client_ref_number),
                    "name": consumer.name,
                    "balance": consumer.balance,
                    "status": consumer.status,
                    "address": consumer.address,
                },
            ],
        }

        self.assertOkResponse(response, expected_payload)

    def test_when_max_balance_param_is_sent_then_returns_expected_consumers(self):
        ConsumerFactory(balance=2000)
        consumer = ConsumerFactory(balance=1000)

        response = self.client.get("/consumers/?max_balance=1000")

        # Names are unique during the tests here
        self.assertFilteredResponse(response, {consumer.name}, key="name")

    def test_when_min_balance_param_is_sent_then_returns_expected_consumers(self):
        consumer = ConsumerFactory(balance=2000)
        ConsumerFactory(balance=1000)

        response = self.client.get("/consumers/?min_balance=2000")

        # Names are unique during the tests here
        self.assertFilteredResponse(response, {consumer.name}, key="name")

    def test_when_consumer_name_param_is_sent_then_returns_expected_consumers(self):
        consumer = ConsumerFactory(name="What So Ever")
        ConsumerFactory(name="Specific Name")

        response = self.client.get("/consumers/?consumer_name=so")

        # Names are unique during the tests here
        self.assertFilteredResponse(response, {consumer.name}, key="name")

    def test_that_it_performs_expected_amount_of_queries(self):
        ConsumerFactory.create_batch(20)

        with self.assertNumQueries(1):
            self.client.get("/consumers/")
