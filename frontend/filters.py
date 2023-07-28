import django_filters
from .models import Bill


class StatementFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(
        field_name="customer_name", lookup_expr='icontains')
    start_bill_date = django_filters.CharFilter(
        field_name="bill_date", lookup_expr='gte')
    end_bill_date = django_filters.DateFilter(
        field_name="bill_date", lookup_expr='lte')
    lr_start_date = django_filters.CharFilter(
        field_name="lr_date", lookup_expr='gte')
    lr_end_date = django_filters.DateFilter(
        field_name="lr_date", lookup_expr='lte')

    class Meta:
        model = Bill
        fields = ['customer_name']
        exclude = ['bill_date', 'lr_date']


class BillFilter(django_filters.FilterSet):
    bill_no = django_filters.CharFilter(
        field_name="bill_no", lookup_expr="icontains")

    class Meta:
        model = Bill
        fields = ''
        exclude = ['bill_no']


class VehicleFilter(django_filters.FilterSet):
    start_location = django_filters.CharFilter(
        field_name="from_field", lookup_expr='icontains')
    end_location = django_filters.CharFilter(
        field_name="to_field", lookup_expr='icontains')

    class Meta:
        model = Bill
        fields = ''
        exclude = ['from_field', 'to_field']
