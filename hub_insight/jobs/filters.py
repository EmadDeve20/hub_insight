from django_filters import FilterSet, CharFilter

from hub_insight.utils.explore.searcher import searcher

class JobFilterSet(FilterSet):
    search = CharFilter(method="filter_search")


    def filter_search(self, queryset, name, value):

        fields = [
            "name",
            "help",
            "variables__name",
        ]

        return searcher(queryset, fields, value)

