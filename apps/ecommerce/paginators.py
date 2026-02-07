from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    def calc_pages(self, page_size:int, object_count:int):
        if object_count  > page_size:
            p = object_count/page_size
            page_count = round(p)
            if object_count % 12!=0:
                page_count+=1
            return page_count
        else:
            return 1
    def get_paginated_response(self, data, status):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_count': self.calc_pages(self.page_size, self.page.paginator.count),
            'results': data,
        }, status=status)
    