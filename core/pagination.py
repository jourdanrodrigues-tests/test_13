from rest_framework.pagination import CursorPagination as DRFCursorPagination


class CursorPagination(DRFCursorPagination):
    page_size_query_param = "page_size"
    ordering = "-created_date"
