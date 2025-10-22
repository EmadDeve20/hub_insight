from django.db.models import Q, QuerySet


def __create_q_object(field, target, operator='__icontains'):
    return Q(**{f"{field}{operator}": target})


def searcher(qs: QuerySet, fields: list[str], target: str, operator: str = '__icontains') -> QuerySet:
    """
    Search in any fields of you want with a given target and operator.

    Args:
        qs (QuerySet): The queryset to filter.
        fields (list[str]): A list of field names to search in.
        target (str): The search target.
        operator (str, optional): The comparison operator (e.g., '__icontains', '__exact', '__startswith'). Defaults to '__icontains'.

    Returns:
        QuerySet: The filtered queryset.
    """

    base = Q()
    for field in fields:
        base |= __create_q_object(field, target, operator)
    return qs.filter(base)

