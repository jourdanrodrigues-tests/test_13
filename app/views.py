from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.filters import ConsumerFilterSet
from app.models import Consumer
from app.serializers import ConsumerSerializer, ConsumerCsvUploadSerializer


class ConsumerViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    filterset_class = ConsumerFilterSet

    @action(detail=False, methods=["POST"], serializer_class=ConsumerCsvUploadSerializer)
    def upload_csv(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data['consumers'], status=status.HTTP_200_OK)
