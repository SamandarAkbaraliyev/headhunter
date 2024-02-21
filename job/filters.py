import django_filters
from job.models import Job


class JobDayModelFilter(django_filters.FilterSet):
    published_at = django_filters.DateTimeFilter(field_name='search_period',
                                                  lookup_expr='gte')

    class Meta:
        model = Job
        fields = ['published_at']
