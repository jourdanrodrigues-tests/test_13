import django_filters

from app.models import Consumer


class ConsumerFilterSet(django_filters.FilterSet):
    consumer_name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    min_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="gte")
    max_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="lte")

    class Meta:
        model = Consumer
        fields = ["min_balance", "max_balance", "consumer_name", "status"]
