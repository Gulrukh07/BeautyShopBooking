from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class GlobalCustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        total_count = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        current_page = self.page.number
        total_pages = math.ceil(total_count / page_size) if page_size else 0

        return Response(
            {
            "items": data,
            "pageNumber": current_page,
            "pageSize": page_size,
            "totalCount": total_count,
            "totalPages": total_pages,
            "total": total_count
            }
        )
