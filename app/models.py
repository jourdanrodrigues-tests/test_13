from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Consumer(models.Model):
    class StatusChoices(models.TextChoices):
        INACTIVE = 'INACTIVE', _('Inactive')
        PAID_IN_FULL = 'PAID_IN_FULL', _('Paid in full')
        IN_COLLECTION = 'IN_COLLECTION', _('In collection')

    ssn = models.CharField(max_length=9, primary_key=True)
    client_ref_number = models.UUIDField()
    name = models.CharField(max_length=255)
    balance = models.IntegerField()
    status = models.CharField(choices=StatusChoices, max_length=13)
    address = models.CharField(max_length=255)
