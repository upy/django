from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from datetime import timedelta, datetime

from posts.enums import Periods


class PostFilter(filters.FilterSet):
    period = filters.ChoiceFilter(label=_("Period"), choices=Periods.choices)

    def filter_period(self, *args, **kwargs):

            if period == 'daily':
                return queryset.filter(**{"pub_date": datetime.today()})
            elif period == 'weekly':
                return queryset.filter(**{"pub_date__gt": datetime.today() - timedelta(days=7)})
            else:
                return queryset.filter(**{"pub_date__gt": datetime.today() - timedelta(days=30)})
        else:
            return queryset

class PostSearchFilter(filters.FilterSet):
    query = filters.CharFilter(label=_("Query"), method="filter_query")

    def filter_query(self, *args, **kwargs):
        import ipdb;ipdb.set_trace()
