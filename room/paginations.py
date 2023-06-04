from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "per_page"

    def paginated_response(self, data):
        return {
            "page": self.page.number,
            "count": self.page.paginator.count,
            "page_size": self.page.paginator.per_page,
            "results": data,
        }

    def paginated_queryset(self, qs, request):
        return super(CustomPagination, self).paginate_queryset(qs, request)
