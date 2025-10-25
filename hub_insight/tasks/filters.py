from django_filters import CharFilter, FilterSet

from hub_insight.utils.explore.searcher import searcher

class JobFilterSet(FilterSet):

    search = CharFilter(method="filter_search")
    is_enabled = CharFilter(method="filter_is_enabled")
    job_ids = CharFilter(method="filter_job_ids")
    user_ids = CharFilter(method="filter_user_ids")

    def filter_search(self, queryset, name, value):
        
        fields = [
            "job__name",
            "job__variables__name",
            "variables"
        ]

        return searcher(queryset, fields, value)
    

    def filter_is_enabled(self, queryset, name, value):

        if value.lower() == "true":
            return  queryset.filter(enabled=True)
        elif value.lower() == "false":
            return  queryset.filter(enabled=False)
        return queryset
    

    def filter_job_ids(self, queryset, name, value):
        
        values = list(map(int, value.split(",")))

        return queryset.filter(job__id__in=values)



    def filter_user_ids(self, queryset, name, value):

        values = list(map(int, value.split(",")))

        return queryset.filter(user__id__in=values)

