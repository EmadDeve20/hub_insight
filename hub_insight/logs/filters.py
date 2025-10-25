from django_filters import CharFilter, FilterSet

from hub_insight.utils.explore.searcher import searcher

class TaskLogFilterSet(FilterSet):

    search = CharFilter(method="filter_search")
    is_enabled = CharFilter(method="filter_is_enabled")
    is_ok = CharFilter(method="filter_is_ok")
    job_ids = CharFilter(method="filter_job_ids")
    user_ids = CharFilter(method="filter_user_ids")
    order_by = CharFilter(method="filter_order_by")
    from_datetime = CharFilter(method="filter_from_datetime")
    to_datetime = CharFilter(method="filter_to_datetime")


    def filter_search(self, queryset, name, value):
        
        fields = [
            "task__job__name",
            "variables",
        ]

        return searcher(queryset, fields, value)
    

    def filter_is_enabled(self, queryset, name, value):

        if value.lower() == "true":
            return  queryset.filter(task__enabled=True)
        elif value.lower() == "false":
            return  queryset.filter(task__enabled=False)
        return queryset
    

    def filter_job_ids(self, queryset, name, value):
        
        values = list(map(int, value.split(",")))

        return queryset.filter(task__job__id__in=values)



    def filter_user_ids(self, queryset, name, value):

        values = list(map(int, value.split(",")))

        return queryset.filter(task__user__id__in=values)


    def filter_order_by(self, queryset, name, value):
        
        values = value.split(",")

        return queryset.order_by(*values)


    def filter_is_ok(self, queryset, name, value):

        if value.lower() == "true":
            return  queryset.filter(is_ok=True)
        elif value.lower() == "false":
            return  queryset.filter(is_ok=False)
        return queryset


    def filter_from_datetime(self, queryset, name, value):
        
        return queryset.filter(created_at__gte=value)
    

    def filter_to_datetime(self, queryset, name, value):
        
        return queryset.filter(created_at__lt=value)


