from rest_framework.test import APITestCase

from app.factories import ConsumerFactory
from app.models import Consumer
from app.tests.utils import TestCaseMixin


class TestGet(TestCaseMixin, APITestCase):
    def test_that_it_returns_expected_response(self):
        consumer = ConsumerFactory()

        response = self.client.get("/consumers/")

        expected_data = {
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

        self.assertOkResponse(response, expected_data)

    def test_when_has_more_than_one_page_then_returns_expected_response(self):
        consumer2 = ConsumerFactory()
        consumer1 = ConsumerFactory()

        def build_consumer_data(consumer: Consumer) -> dict:
            return {
                "client_ref_number": str(consumer.client_ref_number),
                "name": consumer.name,
                "balance": consumer.balance,
                "status": consumer.status,
                "address": consumer.address,
            }

        response1 = self.client.get("/consumers/?page_size=1")

        page2 = response1.data["next"]
        expected_data = {
            'next': page2,
            'previous': None,
            'results': [build_consumer_data(consumer1)],
        }

        self.assertOkResponse(response1, expected_data)

        response2 = self.client.get(page2)
        page1 = response2.data["previous"]
        expected_data = {
            'next': None,
            'previous': page1,
            'results': [build_consumer_data(consumer2)],
        }

        self.assertOkResponse(response2, expected_data)

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
