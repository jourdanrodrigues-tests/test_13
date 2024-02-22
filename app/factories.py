import secrets
from uuid import uuid4

import factory
from factory import fuzzy

from app.models import Consumer


def generate_ssn():
    # First simpler SSN generation I stumbled in the internet
    area_number = secrets.randbelow(900) + 100
    group_number = secrets.randbelow(90) + 10
    serial_number = secrets.randbelow(9000) + 1000
    return f"{area_number:03d}-{group_number:02d}-{serial_number:04d}"


class ConsumerFactory(factory.django.DjangoModelFactory):
    ssn = factory.LazyFunction(generate_ssn)
    client_ref_number = factory.LazyFunction(uuid4)
    name = factory.Sequence(lambda n: f"Consumer {n}")
    balance = factory.LazyFunction(lambda: float(secrets.randbelow(1000)))
    status = fuzzy.FuzzyChoice([choice[0] for choice in Consumer.StatusChoices.choices])
    address = factory.Faker("address")

    class Meta:
        model = Consumer
