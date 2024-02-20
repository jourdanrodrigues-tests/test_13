from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app.filters import ConsumerFilterSet
from app.models import Consumer
from app.serializers import ConsumerSerializer


class ConsumerViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    filterset_class = ConsumerFilterSet
