from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination as _PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.paginator import InvalidPage

class PageNumberPagination(_PageNumberPagination):
    # TODO: Read this from env file
    # page_size = int(REST_FRAMEWORK["PAGE_SIZE"])
    # max_page_size = int(REST_FRAMEWORK["MAX_PAGE_SIZE"])
    
    page_size = 5
    max_page_size = 10
    superuser_max_page_size =100
    
    page_query_param = "p"
    page_size_query_param = "page_size"


    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("page_size", self.get_page_size(self.request)),
                    ("results", data),
                ]
            )
        )

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """

        page_number = request.GET.get("all")
        if page_number == "true":
            return None
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return self.page


    def get_page_size(self, request):
        page_size = request.GET.get(self.page_size_query_param, self.page_size)

        page_size = int(page_size)

        if request.user.is_superuser and page_size >= self.superuser_max_page_size:
            return self.superuser_max_page_size
        
        elif not request.user.is_superuser and page_size >= self.superuser_max_page_size:
            return self.max_page_size
        
        return page_size



def get_paginated_response(serializer_class, queryset, request, view):

    paginator = PageNumberPagination()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)

def get_paginated_response_context(serializer_class, queryset, request, view):
    paginator = PageNumberPagination()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True, context={'request':request})

    return Response(data=serializer.data)

